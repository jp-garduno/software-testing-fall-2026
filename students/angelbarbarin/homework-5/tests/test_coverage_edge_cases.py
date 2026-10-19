"""Edge-case tests written after reading the first coverage report.

The first run left the repository's error handling and search branches, and most of
NotificationService, uncovered. Each class below targets one of those gaps.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import SMS_MAX_LENGTH, NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskRepository


class TestRepositoryCrud:
    def test_save_then_find_by_id_returns_same_task(self, repository, make_task):
        task = make_task()

        assert repository.save(task) is task
        assert repository.find_by_id(task.id) is task

    def test_find_by_id_unknown_returns_none(self, repository):
        assert repository.find_by_id("does-not-exist") is None

    def test_find_by_title_ignores_case_and_spaces(self, repository, make_task):
        task = repository.save(make_task("Review pull request"))

        assert repository.find_by_title("  review PULL request ") is task

    def test_find_by_title_partial_match_is_not_a_match(self, repository, make_task):
        repository.save(make_task("Review pull request"))

        assert repository.find_by_title("Review") is None

    def test_delete_existing_and_missing(self, repository, make_task):
        task = repository.save(make_task())

        assert repository.delete(task.id) is True
        assert repository.delete(task.id) is False


class TestRepositoryErrorHandling:
    """Every database call is wrapped so callers only ever see RepositoryError."""

    @pytest.fixture(name="broken_repository")
    def fixture_broken_repository(self):
        database = Mock()
        failure = ConnectionError("database unreachable")
        database.upsert.side_effect = failure
        database.get.side_effect = failure
        database.values.side_effect = failure
        database.remove.side_effect = failure
        return TaskRepository(database)

    def test_save_failure_is_wrapped(self, broken_repository, make_task):
        with pytest.raises(RepositoryError, match="Could not save task") as error:
            broken_repository.save(make_task())
        assert isinstance(error.value.__cause__, ConnectionError)

    def test_find_by_id_failure_is_wrapped(self, broken_repository):
        with pytest.raises(RepositoryError, match="Could not read task abc"):
            broken_repository.find_by_id("abc")

    def test_find_all_failure_is_wrapped(self, broken_repository):
        with pytest.raises(RepositoryError, match="Could not list tasks"):
            broken_repository.find_all()

    def test_find_by_title_propagates_list_failure(self, broken_repository):
        with pytest.raises(RepositoryError):
            broken_repository.find_by_title("anything")

    def test_delete_failure_is_wrapped(self, broken_repository):
        with pytest.raises(RepositoryError, match="Could not delete task abc"):
            broken_repository.delete("abc")


class TestRepositorySearchBranches:
    @pytest.fixture(name="populated")
    def fixture_populated(self, repository):
        now = datetime.now()
        tasks = {
            "soon": Task("Pay rent", priority=TaskPriority.HIGH, due_date=now + timedelta(days=2)),
            "later": Task("Pay taxes", priority=TaskPriority.URGENT, due_date=now + timedelta(days=30)),
            "undated": Task("Read a book", priority=TaskPriority.LOW),
        }
        tasks["later"].transition_to(TaskStatus.IN_PROGRESS)
        for task in tasks.values():
            repository.save(task)
        return repository, tasks, now

    def test_search_without_filters_returns_all(self, populated):
        repository, tasks, _ = populated
        assert len(repository.search()) == len(tasks)

    def test_search_by_due_after_excludes_undated_tasks(self, populated):
        repository, tasks, now = populated
        assert repository.search(due_after=now + timedelta(days=10)) == [tasks["later"]]

    def test_search_by_due_before(self, populated):
        repository, tasks, now = populated
        assert repository.search(due_before=now + timedelta(days=10)) == [tasks["soon"]]

    def test_search_date_range_is_inclusive(self, populated):
        repository, tasks, _ = populated
        due = tasks["soon"].due_date
        assert repository.search(due_after=due, due_before=due) == [tasks["soon"]]

    def test_search_inverted_date_range_is_rejected(self, populated):
        repository, _, now = populated
        with pytest.raises(ValueError, match="due_after"):
            repository.search(due_after=now + timedelta(days=5), due_before=now)

    def test_search_blank_title_filter_is_ignored(self, populated):
        repository, tasks, _ = populated
        assert len(repository.search(title_contains="   ")) == len(tasks)

    def test_search_combines_all_filters(self, populated):
        repository, tasks, now = populated

        result = repository.search(
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.URGENT,
            due_after=now,
            due_before=now + timedelta(days=60),
            title_contains="PAY",
        )

        assert result == [tasks["later"]]

    def test_search_with_no_matches_returns_empty_list(self, populated):
        repository, _, _ = populated
        assert not repository.search(status=TaskStatus.DONE)


class TestNotificationValidation:
    def test_constructor_rejects_negative_retries(self, email_client, sms_client):
        with pytest.raises(ValueError, match="max_retries"):
            NotificationService(email_client, sms_client, max_retries=-1)

    @pytest.mark.parametrize("recipient", ["", None, "no-at-sign.com", "a@b", "two@@example.com"])
    def test_send_email_rejects_invalid_address(self, notifier, email_client, recipient):
        with pytest.raises(NotificationError, match="Invalid email"):
            notifier.send_email(recipient, "Subject", "Body")
        email_client.send.assert_not_called()

    def test_send_email_requires_subject(self, notifier, email_client):
        with pytest.raises(NotificationError, match="subject is required"):
            notifier.send_email("user@example.com", "", "Body")
        email_client.send.assert_not_called()

    @pytest.mark.parametrize("phone", ["", None, "12345", "33-1234-5678", "+1234567890123456"])
    def test_send_sms_rejects_invalid_phone(self, notifier, sms_client, phone):
        with pytest.raises(NotificationError, match="Invalid phone"):
            notifier.send_sms(phone, "Hello")
        sms_client.send.assert_not_called()

    def test_send_sms_at_limit_is_not_truncated(self, notifier, sms_client):
        text = "x" * SMS_MAX_LENGTH
        notifier.send_sms("+523312345678", text)
        sms_client.send.assert_called_once_with("+523312345678", text)

    def test_send_sms_over_limit_is_truncated_with_ellipsis(self, notifier, sms_client):
        notifier.send_sms("3312345678", "y" * (SMS_MAX_LENGTH + 1))

        sent = sms_client.send.call_args.args[1]
        assert len(sent) == SMS_MAX_LENGTH
        assert sent.endswith("...")


class TestNotificationMessages:
    def test_notify_task_created_formats_email(self, notifier, email_client):
        notifier.notify_task_created("user@example.com", Task("Write report"))
        email_client.send.assert_called_once_with(
            "user@example.com", "New Task Created", "Task 'Write report' has been created"
        )

    def test_notify_status_change_includes_both_statuses(self, notifier, email_client):
        task = Task("Write report")
        old = task.transition_to(TaskStatus.IN_PROGRESS)

        notifier.notify_status_change("user@example.com", task, old)

        body = email_client.send.call_args.args[2]
        assert "from TODO to IN_PROGRESS" in body

    def test_notify_overdue_formats_email(self, notifier, email_client):
        notifier.notify_overdue("user@example.com", Task("Late report"))
        assert email_client.send.call_args.args[1:] == ("Task Overdue", "Task 'Late report' is overdue!")

    def test_notify_urgent_sms(self, notifier, sms_client):
        notifier.notify_urgent_sms("+523312345678", Task("Fix prod", priority=TaskPriority.URGENT))
        sms_client.send.assert_called_once_with("+523312345678", "URGENT task: Fix prod")
