"""Edge cases added after reading the coverage report.

They target branches of the repository, the notification service and the
service layer that the workflow tests do not reach.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskRepository
from task_service import TaskService


# ======================================================= TaskRepository (real, dict-backed)
class TestTaskRepository:
    @pytest.fixture
    def repo(self):
        return TaskRepository({})

    def test_save_assigns_incrementing_ids(self, repo):
        first, second = Task("First task"), Task("Second task")
        repo.save(first)
        repo.save(second)
        assert (first.id, second.id) == (1, 2)

    def test_save_existing_task_keeps_id(self, repo):
        task = repo.save(Task("Stable id"))
        task.description = "changed"
        repo.save(task)
        assert task.id == 1
        assert len(repo.find_all()) == 1

    def test_find_by_id_hit_and_miss(self, repo):
        task = repo.save(Task("Findable"))
        assert repo.find_by_id(task.id) is task
        assert repo.find_by_id(999) is None

    def test_find_by_title_is_exact(self, repo):
        task = repo.save(Task("Exact title"))
        assert repo.find_by_title("Exact title") is task
        assert repo.find_by_title("Exact") is None

    def test_delete_removes_task_permanently(self, repo):
        task = repo.save(Task("Remove me"))
        assert repo.delete(task.id) is True
        assert repo.find_by_id(task.id) is None

    def test_delete_missing_task_returns_false(self, repo):
        assert repo.delete(42) is False

    def test_database_failure_on_save_is_wrapped(self):
        db = Mock()
        db.__setitem__ = Mock(side_effect=OSError("write failed"))
        with pytest.raises(RepositoryError, match="Could not save"):
            TaskRepository(db).save(Task("Will fail"))

    def test_database_failure_on_delete_is_wrapped(self):
        db = Mock()
        db.__contains__ = Mock(side_effect=OSError("read failed"))
        with pytest.raises(RepositoryError, match="Could not delete"):
            TaskRepository(db).delete(1)

    def test_database_failure_on_find_all_is_wrapped(self):
        db = Mock()
        db.values.side_effect = OSError("read failed")
        with pytest.raises(RepositoryError, match="Could not read"):
            TaskRepository(db).find_all()


class TestRepositorySearch:
    @pytest.fixture
    def repo(self):
        repo = TaskRepository({})
        now = datetime.now()
        a = Task("Write report", priority=TaskPriority.HIGH, due_date=now + timedelta(days=2))
        b = Task("Review code", priority=TaskPriority.LOW, due_date=now + timedelta(days=10))
        c = Task("Report bug", priority=TaskPriority.HIGH)  # no due date
        c.status = TaskStatus.IN_PROGRESS
        for task in (a, b, c):
            repo.save(task)
        return repo

    def titles(self, tasks):
        return sorted(t.title for t in tasks)

    def test_no_filters_returns_everything(self, repo):
        assert len(repo.search()) == 3

    def test_filter_by_status(self, repo):
        assert self.titles(repo.search(status=TaskStatus.IN_PROGRESS)) == ["Report bug"]

    def test_filter_by_priority(self, repo):
        assert self.titles(repo.search(priority=TaskPriority.HIGH)) == ["Report bug", "Write report"]

    def test_filter_by_title_is_partial_and_case_insensitive(self, repo):
        assert self.titles(repo.search(title_contains="REPORT")) == ["Report bug", "Write report"]

    def test_filter_by_due_from(self, repo):
        later = datetime.now() + timedelta(days=5)
        assert self.titles(repo.search(due_from=later)) == ["Review code"]

    def test_filter_by_due_to(self, repo):
        sooner = datetime.now() + timedelta(days=5)
        assert self.titles(repo.search(due_to=sooner)) == ["Write report"]

    def test_filter_by_date_range_excludes_tasks_without_due_date(self, repo):
        now = datetime.now()
        result = repo.search(due_from=now, due_to=now + timedelta(days=30))
        assert self.titles(result) == ["Review code", "Write report"]

    def test_combined_filters(self, repo):
        result = repo.search(priority=TaskPriority.HIGH, title_contains="write")
        assert self.titles(result) == ["Write report"]

    def test_filters_with_no_match(self, repo):
        assert repo.search(status=TaskStatus.DONE) == []


# ======================================================= NotificationService
class TestNotificationService:
    def test_send_email_delivers_through_transport(self):
        transport = Mock(return_value="ok")
        service = NotificationService(transport)

        assert service.send_email("a@b.com", "Hi", "Body") == "ok"
        transport.assert_called_once_with("email", "a@b.com", {"subject": "Hi", "body": "Body"})

    def test_send_sms_delivers_through_transport(self):
        transport = Mock(return_value="sent")
        service = NotificationService(transport)

        assert service.send_sms("+521234567890", "Hello") == "sent"
        transport.assert_called_once_with("sms", "+521234567890", {"message": "Hello"})

    @pytest.mark.parametrize("address", ["", None, "no-at-sign"])
    def test_invalid_email_is_rejected(self, address):
        transport = Mock()
        with pytest.raises(NotificationError, match="Invalid email"):
            NotificationService(transport).send_email(address, "s", "b")
        transport.assert_not_called()

    @pytest.mark.parametrize("number", ["", None, "abc", "+12ab"])
    def test_invalid_phone_is_rejected(self, number):
        with pytest.raises(NotificationError, match="Invalid phone"):
            NotificationService(Mock()).send_sms(number, "msg")

    def test_missing_transport_raises(self):
        with pytest.raises(NotificationError, match="No transport"):
            NotificationService().send_email("a@b.com", "s", "b")

    def test_transient_failure_is_retried(self):
        transport = Mock(side_effect=[ConnectionError("blip"), "delivered"])
        assert NotificationService(transport).send_email("a@b.com", "s", "b") == "delivered"
        assert transport.call_count == 2

    def test_gives_up_after_max_retries(self):
        transport = Mock(side_effect=ConnectionError("down"))
        service = NotificationService(transport, max_retries=3)

        with pytest.raises(NotificationError, match="after 3 attempts"):
            service.send_email("a@b.com", "s", "b")
        assert transport.call_count == 3


# ======================================================= TaskService edge cases
class TestServiceEdgeCases:
    def test_update_task_only_priority_leaves_other_fields(self, task_service, mock_repository):
        task = Task("Untouched", "keep me", TaskPriority.LOW)
        mock_repository.find_by_id.return_value = task

        task_service.update_task(1, priority=TaskPriority.URGENT)

        assert (task.title, task.description) == ("Untouched", "keep me")
        assert task.priority == TaskPriority.URGENT
        mock_repository.find_by_title.assert_not_called()

    def test_update_task_can_clear_due_date(self, task_service, mock_repository):
        task = Task("Has due date", due_date=datetime.now() + timedelta(days=1))
        mock_repository.find_by_id.return_value = task

        task_service.update_task(1, due_date=None)

        assert task.due_date is None

    def test_update_task_truncates_long_description(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Long text")

        updated = task_service.update_task(1, description="y" * 800)

        assert len(updated.description) == 500

    def test_update_task_rejects_invalid_title(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Valid title")

        with pytest.raises(ValueError, match="at least 3 characters"):
            task_service.update_task(1, title="x")

    def test_service_with_real_repository_end_to_end(self):
        """Light end-to-end check using the real repository over a dict database."""
        notifier = Mock(spec=NotificationService)
        service = TaskService(TaskRepository({}), notifier)

        task = service.create_task("Real repo task")
        service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert service.get_task(task.id).status == TaskStatus.IN_PROGRESS
        assert notifier.send_email.call_count == 2
