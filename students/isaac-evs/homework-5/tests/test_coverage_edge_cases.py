"""Targeted tests for branches found uncovered by the coverage report.

Each test names the branch it exists to exercise. Gateway and repository logic is tested
directly here because the service tests mock those layers away.
"""

from datetime import timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskRepository


class TestNotificationServiceBranches:
    def test_email_without_configured_client_raises(self):
        with pytest.raises(NotificationError, match="Email client is not configured"):
            NotificationService().send_email("a@b.test", "Hi", "Body")

    def test_email_without_recipient_raises(self):
        service = NotificationService(email_client=Mock())

        with pytest.raises(ValueError, match="Recipient is required"):
            service.send_email("", "Hi", "Body")

    def test_email_returns_the_client_result(self):
        client = Mock()
        client.send.return_value = "queued"

        assert NotificationService(email_client=client).send_email("a@b.test", "s", "b") == "queued"

    def test_sms_without_configured_client_raises(self):
        with pytest.raises(NotificationError, match="SMS client is not configured"):
            NotificationService().send_sms("+15550001", "Hello")

    def test_sms_without_phone_number_raises(self):
        service = NotificationService(sms_client=Mock())

        with pytest.raises(ValueError, match="Phone number is required"):
            service.send_sms("", "Hello")

    def test_sms_client_failure_is_wrapped(self):
        client = Mock()
        client.send.side_effect = ConnectionError("no signal")

        with pytest.raises(NotificationError, match="SMS delivery failed"):
            NotificationService(sms_client=client).send_sms("+15550001", "Hello")


class TestRepositoryFindByTitle:
    @pytest.fixture
    def repository(self, fake_database):
        repo = TaskRepository(fake_database)
        repo.save(Task("Write Report"))
        return repo

    def test_match_ignores_case_and_surrounding_whitespace(self, repository):
        assert repository.find_by_title("  write report ").title == "Write Report"

    def test_returns_none_when_no_title_matches(self, repository):
        assert repository.find_by_title("Something else") is None


class TestRepositorySearchBranches:
    @pytest.fixture
    def repository(self, fake_database, now):
        repo = TaskRepository(fake_database)
        early = Task("Early", priority=TaskPriority.LOW, due_date=now + timedelta(days=1), now=now)
        late = Task("Late", priority=TaskPriority.HIGH, due_date=now + timedelta(days=9), now=now)
        undated = Task("Undated", priority=TaskPriority.HIGH, now=now)
        done = Task("Done thing", now=now)
        done.status = TaskStatus.DONE
        for task in (early, late, undated, done):
            repo.save(task)
        return repo

    def test_no_filters_returns_everything(self, repository):
        assert len(repository.search()) == 4

    def test_status_filter_excludes_other_statuses(self, repository):
        assert [t.title for t in repository.search(status=TaskStatus.DONE)] == ["Done thing"]

    def test_priority_filter_excludes_other_priorities(self, repository):
        titles = {t.title for t in repository.search(priority=TaskPriority.HIGH)}
        assert titles == {"Late", "Undated"}

    def test_due_from_excludes_earlier_and_undated_tasks(self, repository, now):
        titles = [t.title for t in repository.search(due_from=now + timedelta(days=5))]
        assert titles == ["Late"]

    def test_due_to_excludes_later_and_undated_tasks(self, repository, now):
        titles = [t.title for t in repository.search(due_to=now + timedelta(days=5))]
        assert titles == ["Early"]

    def test_due_date_bounds_are_inclusive(self, repository, now):
        exact = now + timedelta(days=1)
        assert [t.title for t in repository.search(due_from=exact, due_to=exact)] == ["Early"]

    def test_title_filter_excludes_non_matching_titles(self, repository):
        assert [t.title for t in repository.search(title_contains="ate")] == ["Late", "Undated"]


class TestRepositoryErrorWrapping:
    @pytest.mark.parametrize(
        "operation, args",
        [
            ("find_by_id", (1,)),
            ("find_all", ()),
            ("delete", (1,)),
            ("find_by_title", ("Any title",)),
            ("search", ()),
        ],
    )
    def test_every_operation_wraps_database_failures(self, operation, args):
        database = Mock()
        database.get.side_effect = OSError("boom")
        database.all.side_effect = OSError("boom")
        database.remove.side_effect = OSError("boom")
        repository = TaskRepository(database)

        with pytest.raises(RepositoryError, match="boom"):
            getattr(repository, operation)(*args)


class TestServiceBranches:
    def test_create_rejects_duplicate_title_found_through_real_repository(self, fake_service):
        service, _, _ = fake_service
        service.create_task("Unique title")

        with pytest.raises(ValueError, match="already exists"):
            service.create_task("unique TITLE")

    def test_description_is_truncated_on_update(self, fake_service):
        service, _, _ = fake_service
        task = service.create_task("Long description")

        assert len(service.update_task(task.id, description="d" * 900).description) == 500

    def test_rename_to_title_with_surrounding_spaces_still_detects_duplicates(self, fake_service):
        service, _, _ = fake_service
        service.create_task("Occupied name")
        other = service.create_task("Free name")

        with pytest.raises(ValueError, match="already exists"):
            service.update_task(other.id, title="  Occupied name ")

    def test_update_with_no_fields_still_refreshes_updated_at(self, fake_service, now):
        service, _, _ = fake_service
        task = service.create_task("Touch only")
        task.updated_at = now - timedelta(days=5)

        assert service.update_task(task.id).updated_at == now

    def test_same_task_detected_by_id_when_repository_returns_a_copy(self, task_service, mock_repository):
        stored = Task("Original name")
        stored.id = 7
        copy = Task("Original name")
        copy.id = 7
        mock_repository.find_by_id.return_value = stored
        mock_repository.find_by_title.return_value = copy

        assert task_service.update_task(7, title="Original name") is stored

    def test_different_task_with_unset_id_is_a_duplicate(self, task_service, mock_repository):
        stored = Task("Task A")
        stored.id = 1
        other = Task("Task B")
        mock_repository.find_by_id.return_value = stored
        mock_repository.find_by_title.return_value = other

        with pytest.raises(ValueError, match="already exists"):
            task_service.update_task(1, title="Task B")
