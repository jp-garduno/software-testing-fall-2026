"""Edge cases chosen from the coverage report: each test targets a branch the
happy-path suites did not reach (boundaries, empty inputs, defaults and error paths)."""

from datetime import timedelta
from unittest.mock import Mock

import pytest

from conftest import NOW
from notification_service import SMS_MAX_LENGTH, NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskQuery, TaskRepository
from task_service import Recipient, TaskService


def task_due(days, title="Due task", priority=TaskPriority.LOW, status=TaskStatus.TODO):
    task = Task(title, priority=priority, due_date=NOW + timedelta(days=days), now=NOW)
    task.status = status
    return task


class TestTaskQuery:

    def test_empty_query_matches_everything(self):
        assert TaskQuery().matches(Task("Anything", now=NOW))

    def test_status_mismatch(self):
        assert not TaskQuery(status=TaskStatus.DONE).matches(task_due(1))

    def test_priority_mismatch(self):
        assert not TaskQuery(priority=TaskPriority.URGENT).matches(task_due(1))

    def test_task_without_due_date_never_matches_a_date_range(self):
        assert not TaskQuery(due_after=NOW).matches(Task("No date", now=NOW))

    @pytest.mark.parametrize(
        "days, expected",
        [(1, False), (2, True), (5, True), (6, False)],
        ids=["before-range", "lower-bound", "upper-bound", "after-range"],
    )
    def test_date_range_bounds_are_inclusive(self, days, expected):
        query = TaskQuery(due_after=NOW + timedelta(days=2), due_before=NOW + timedelta(days=5))
        assert query.matches(task_due(days)) is expected

    def test_open_ended_date_ranges(self):
        assert TaskQuery(due_after=NOW + timedelta(days=1)).matches(task_due(30))
        assert TaskQuery(due_before=NOW + timedelta(days=1)).matches(task_due(1))
        assert not TaskQuery(due_before=NOW + timedelta(days=1)).matches(task_due(2))

    def test_inverted_date_range_is_rejected(self):
        with pytest.raises(ValueError, match="must not be later"):
            TaskQuery(due_after=NOW + timedelta(days=5), due_before=NOW)

    def test_title_search_is_partial_and_case_insensitive(self):
        task = Task("Quarterly REPORT draft", now=NOW)
        assert TaskQuery(title_contains="report").matches(task)
        assert not TaskQuery(title_contains="invoice").matches(task)

    def test_all_criteria_combined(self):
        task = task_due(3, title="Release notes", priority=TaskPriority.HIGH, status=TaskStatus.IN_PROGRESS)
        query = TaskQuery(status=TaskStatus.IN_PROGRESS, priority=TaskPriority.HIGH, due_after=NOW,
                          due_before=NOW + timedelta(days=4), title_contains="notes")
        assert query.matches(task)


class TestTaskRepository:
    """The real repository against a mocked database client."""

    @pytest.fixture(name="database")
    def fixture_database(self):
        return Mock()

    @pytest.fixture(name="repository")
    def fixture_repository(self, database):
        return TaskRepository(database)

    def test_save_puts_task_under_its_id(self, repository, database):
        task = Task("Saved task", now=NOW)
        assert repository.save(task) is task
        database.put.assert_called_once_with(task.id, task)

    def test_find_by_id(self, repository, database):
        database.get.return_value = "stored"
        assert repository.find_by_id("abc") == "stored"
        database.get.assert_called_once_with("abc")

    def test_find_by_title_exact_match_only(self, repository, database):
        task = Task("Exact title", now=NOW)
        database.values.return_value = [task]
        assert repository.find_by_title("Exact title") is task
        assert repository.find_by_title("exact title") is None

    def test_delete_existing_task(self, repository, database):
        database.get.return_value = Task("Doomed", now=NOW)
        assert repository.delete("abc") is True
        database.remove.assert_called_once_with("abc")

    def test_delete_missing_task_returns_false(self, repository, database):
        database.get.return_value = None
        assert repository.delete("abc") is False
        database.remove.assert_not_called()

    def test_search_filters_stored_tasks(self, repository, database):
        done = task_due(1, title="Done task", status=TaskStatus.DONE)
        database.values.return_value = [task_due(1), done]
        assert repository.search(TaskQuery(status=TaskStatus.DONE)) == [done]

    @pytest.mark.parametrize("operation, call", [
        ("put", lambda repo: repo.save(Task("Any task", now=NOW))),
        ("get", lambda repo: repo.find_by_id("x")),
        ("values", lambda repo: repo.find_all()),
    ])
    def test_database_errors_are_wrapped(self, repository, database, operation, call):
        getattr(database, operation).side_effect = ConnectionError("network down")

        with pytest.raises(RepositoryError, match=f"Database {operation} failed: network down") as info:
            call(repository)

        assert isinstance(info.value.__cause__, ConnectionError)


class TestNotificationService:
    """The real notification service against mocked provider clients."""

    @pytest.fixture(name="clients")
    def fixture_clients(self):
        return Mock(), Mock()

    @pytest.fixture(name="service")
    def fixture_service(self, clients):
        return NotificationService(*clients)

    def test_send_email_calls_provider(self, service, clients):
        clients[0].send.return_value = "msg-1"
        assert service.send_email("ana@example.com", "Hi", "Body") == "msg-1"
        clients[0].send.assert_called_once_with(to="ana@example.com", subject="Hi", body="Body")

    @pytest.mark.parametrize("recipient", ["", None, "no-at-sign", "a@b", "two@@example.com"])
    def test_invalid_email_recipient_is_rejected_before_calling_provider(self, service, clients, recipient):
        with pytest.raises(NotificationError, match="Invalid email"):
            service.send_email(recipient, "Hi", "Body")
        clients[0].send.assert_not_called()

    def test_email_without_subject_is_rejected(self, service):
        with pytest.raises(NotificationError, match="subject is required"):
            service.send_email("ana@example.com", "", "Body")

    def test_email_provider_failure_is_wrapped(self, service, clients):
        clients[0].send.side_effect = TimeoutError("SMTP timeout")
        with pytest.raises(NotificationError, match="Email delivery failed: SMTP timeout"):
            service.send_email("ana@example.com", "Hi", "Body")

    def test_send_sms_calls_provider(self, service, clients):
        service.send_sms("+523312345678", "Short message")
        clients[1].send.assert_called_once_with(to="+523312345678", message="Short message")

    @pytest.mark.parametrize("phone", ["", None, "123", "phone-number", "+52 33 1234 5678"])
    def test_invalid_phone_is_rejected(self, service, clients, phone):
        with pytest.raises(NotificationError, match="Invalid phone"):
            service.send_sms(phone, "Hi")
        clients[1].send.assert_not_called()

    def test_sms_at_max_length_is_sent_unchanged(self, service, clients):
        message = "x" * SMS_MAX_LENGTH
        service.send_sms("3312345678", message)
        assert clients[1].send.call_args.kwargs["message"] == message

    def test_long_sms_is_truncated(self, service, clients):
        service.send_sms("3312345678", "x" * (SMS_MAX_LENGTH + 40))
        sent = clients[1].send.call_args.kwargs["message"]
        assert len(sent) == SMS_MAX_LENGTH
        assert sent.endswith("...")

    def test_sms_provider_failure_is_wrapped(self, service, clients):
        clients[1].send.side_effect = RuntimeError("carrier down")
        with pytest.raises(NotificationError, match="SMS delivery failed: carrier down"):
            service.send_sms("3312345678", "Hi")


class TestTaskServiceEdgeCases:

    def test_defaults_use_real_clock_and_default_recipient(self, mock_repository, mock_notification_service):
        service = TaskService(mock_repository, mock_notification_service)

        task = service.create_task("Default service task")

        assert service.recipient == Recipient()
        assert task.created_at > NOW - timedelta(days=36500)
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "New Task Created", "Task 'Default service task' has been created"
        )

    def test_update_unknown_field_is_rejected(self, task_service, mock_repository):
        with pytest.raises(ValueError, match="Cannot update field\\(s\\): id, status"):
            task_service.update_task("id", status=TaskStatus.DONE, id="new")
        mock_repository.find_by_id.assert_not_called()

    def test_update_description_to_none_clears_it(self, task_service, mock_repository):
        task = Task("Described", "Old text", now=NOW)
        mock_repository.find_by_id.return_value = task

        task_service.update_task(task.id, description=None)

        assert task.description == ""

    def test_update_due_date_to_none_removes_it(self, task_service, mock_repository):
        task = task_due(3)
        mock_repository.find_by_id.return_value = task

        task_service.update_task(task.id, due_date=None)

        assert task.due_date is None

    def test_update_with_too_long_description_is_rejected(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Described", now=NOW)
        with pytest.raises(ValueError, match="not exceed 500"):
            task_service.update_task("id", description="d" * 501)
        mock_repository.save.assert_not_called()

    def test_update_with_invalid_title_is_rejected(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Described", now=NOW)
        with pytest.raises(ValueError, match="at least 3"):
            task_service.update_task("id", title="x")
        mock_repository.find_by_title.assert_not_called()

    def test_update_with_no_changes_only_touches_timestamp(self, task_service, mock_repository):
        task = Task("Untouched", now=NOW - timedelta(days=1))
        mock_repository.find_by_id.return_value = task

        task_service.update_task(task.id)

        assert task.updated_at == NOW
        mock_repository.save.assert_called_once_with(task)

    def test_done_task_past_due_is_not_reported_overdue(self, task_service, mock_repository,
                                                        mock_notification_service):
        task = task_due(1, status=TaskStatus.DONE)
        task.due_date = NOW - timedelta(days=1)
        mock_repository.find_all.return_value = [task]

        assert not task_service.check_overdue_tasks()
        mock_notification_service.send_email.assert_not_called()
