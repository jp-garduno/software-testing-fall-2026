"""Part 3 - Tests written from the coverage report to close branch gaps.

They target the repository's search/filter branches, the database error
wrapping and the validation branches of the notification service.
"""

from datetime import timedelta
from unittest.mock import Mock

import pytest
from conftest import NEXT_WEEK, NOW, TOMORROW

from errors import NotificationError, RepositoryError
from notification_service import SMS_MAX_LENGTH, NotificationService
from task import TaskPriority, TaskStatus
from task_repository import TaskRepository


@pytest.fixture(name="populated")
def populated_fixture(fake_repository, make_task):
    """Four tasks covering every filter dimension."""
    tasks = {
        "report": make_task("Write report", priority=TaskPriority.HIGH, due_date=TOMORROW),
        "tests": make_task("Write tests", priority=TaskPriority.URGENT, due_date=NEXT_WEEK),
        "read": make_task("Read book", priority=TaskPriority.LOW),
        "call": make_task("Call client", priority=TaskPriority.HIGH, due_date=NOW + timedelta(days=3)),
    }
    tasks["tests"].status = TaskStatus.IN_PROGRESS
    for task in tasks.values():
        fake_repository.save(task)
    return tasks


def titles(tasks):
    return sorted(t.title for t in tasks)


class TestRepositorySearch:
    def test_no_filters_returns_everything(self, fake_repository, populated):
        assert len(fake_repository.search()) == len(populated)

    @pytest.mark.usefixtures("populated")
    def test_filter_by_status(self, fake_repository):
        assert titles(fake_repository.search(status=TaskStatus.IN_PROGRESS)) == ["Write tests"]

    @pytest.mark.usefixtures("populated")
    def test_filter_by_priority(self, fake_repository):
        assert titles(fake_repository.search(priority=TaskPriority.HIGH)) == ["Call client", "Write report"]

    @pytest.mark.usefixtures("populated")
    def test_filter_by_date_range_is_inclusive(self, fake_repository):
        result = fake_repository.search(due_from=TOMORROW, due_to=NOW + timedelta(days=3))
        assert titles(result) == ["Call client", "Write report"]

    @pytest.mark.usefixtures("populated")
    def test_filter_only_due_from(self, fake_repository):
        assert titles(fake_repository.search(due_from=NOW + timedelta(days=2))) == ["Call client", "Write tests"]

    @pytest.mark.usefixtures("populated")
    def test_filter_only_due_to_excludes_tasks_without_date(self, fake_repository):
        assert titles(fake_repository.search(due_to=TOMORROW)) == ["Write report"]

    @pytest.mark.usefixtures("populated")
    def test_search_by_partial_title_case_insensitive(self, fake_repository):
        assert titles(fake_repository.search(title_contains="WRITE")) == ["Write report", "Write tests"]

    @pytest.mark.usefixtures("populated")
    def test_combined_filters(self, fake_repository):
        result = fake_repository.search(status=TaskStatus.TODO, priority=TaskPriority.HIGH, title_contains="client")
        assert titles(result) == ["Call client"]

    @pytest.mark.usefixtures("populated")
    def test_no_match_returns_empty_list(self, fake_repository):
        assert not fake_repository.search(title_contains="nothing like this")

    def test_find_by_title_exact_and_missing(self, fake_repository, populated):
        assert fake_repository.find_by_title("  write REPORT ") is populated["report"]
        assert fake_repository.find_by_title("Write") is None

    def test_delete_returns_whether_something_was_removed(self, fake_repository, populated):
        assert fake_repository.delete(populated["read"].task_id) is True
        assert fake_repository.delete(populated["read"].task_id) is False


class TestRepositoryErrorHandling:
    @pytest.mark.parametrize(
        "method, args, db_operation",
        [
            ("save", (Mock(task_id="1"),), "put"),
            ("find_by_id", ("1",), "get"),
            ("find_all", (), "values"),
            ("delete", ("1",), "delete"),
        ],
    )
    def test_database_errors_are_wrapped(self, method, args, db_operation):
        database = Mock()
        getattr(database, db_operation).side_effect = TimeoutError("timeout")
        repository = TaskRepository(database)

        with pytest.raises(RepositoryError, match=f"'{db_operation}' failed: timeout") as info:
            getattr(repository, method)(*args)
        assert isinstance(info.value.__cause__, TimeoutError)

    def test_save_returns_task_and_uses_id_as_key(self):
        database = Mock()
        task = Mock(task_id="abc")
        assert TaskRepository(database).save(task) is task
        database.put.assert_called_once_with("abc", task)


class TestNotificationService:
    @pytest.fixture
    def clients(self):
        return Mock(name="email_client"), Mock(name="sms_client")

    @pytest.fixture
    def service(self, clients):
        return NotificationService(*clients)

    def test_send_email_delegates_to_client(self, service, clients):
        assert service.send_email("ana@example.com", "Hi", "Body") is True
        clients[0].send.assert_called_once_with(to="ana@example.com", subject="Hi", body="Body")

    @pytest.mark.parametrize("recipient", ["", None, "no-at-sign", "a@b", "a b@c.com"])
    def test_send_email_rejects_invalid_recipient(self, service, clients, recipient):
        with pytest.raises(NotificationError, match="Invalid email"):
            service.send_email(recipient, "Hi", "Body")
        clients[0].send.assert_not_called()

    def test_send_email_requires_subject(self, service):
        with pytest.raises(NotificationError, match="subject"):
            service.send_email("ana@example.com", "", "Body")

    def test_send_email_wraps_client_failure(self, service, clients):
        clients[0].send.side_effect = OSError("SMTP unavailable")
        with pytest.raises(NotificationError, match="SMTP unavailable"):
            service.send_email("ana@example.com", "Hi", "Body")

    def test_send_sms_delegates_to_client(self, service, clients):
        assert service.send_sms("+523312345678", "Hello") is True
        clients[1].send.assert_called_once_with(to="+523312345678", message="Hello")

    @pytest.mark.parametrize("phone", ["", None, "12345", "phone-number", "+52 33 1234 5678"])
    def test_send_sms_rejects_invalid_phone(self, service, clients, phone):
        with pytest.raises(NotificationError, match="Invalid phone"):
            service.send_sms(phone, "Hello")
        clients[1].send.assert_not_called()

    def test_long_sms_is_truncated_to_160_characters(self, service, clients):
        service.send_sms("3312345678", "x" * 200)
        sent = clients[1].send.call_args.kwargs["message"]
        assert len(sent) == SMS_MAX_LENGTH
        assert sent.endswith("...")

    def test_sms_of_exactly_160_characters_is_not_truncated(self, service, clients):
        service.send_sms("3312345678", "y" * SMS_MAX_LENGTH)
        assert clients[1].send.call_args.kwargs["message"] == "y" * SMS_MAX_LENGTH

    def test_send_sms_wraps_client_failure(self, service, clients):
        clients[1].send.side_effect = ConnectionError("provider down")
        with pytest.raises(NotificationError, match="provider down"):
            service.send_sms("3312345678", "Hello")
