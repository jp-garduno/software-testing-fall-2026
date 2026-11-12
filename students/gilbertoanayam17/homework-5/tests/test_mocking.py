"""Mocking and isolation: external boundaries replaced by doubles, failures injected with side_effect."""

import logging
from datetime import datetime
from unittest.mock import ANY, Mock, call, patch

import pytest

from notification_service import NotificationError
from task import Task, TaskPriority, TaskStatus
from task_repository import Database, DatabaseError, RepositoryError, TaskRepository

GATEWAY = "https://api.notify.example.com"


class TestNotificationServiceWithMockedGateway:
    def test_send_email_posts_payload_and_returns_message_id(self, notifier, http_client):
        message_id = notifier.send_email("ana@example.com", "Hello", "Body text")

        assert message_id == "msg-1"
        http_client.post.assert_called_once_with(
            f"{GATEWAY}/email", json={"to": "ana@example.com", "subject": "Hello", "body": "Body text"}, timeout=5
        )

    def test_send_sms_truncates_messages_over_160_characters(self, notifier, http_client):
        notifier.send_sms("+523312345678", "x" * 200)

        sent = http_client.post.call_args.kwargs["json"]["message"]
        assert len(sent) == 160
        assert sent.endswith("...")

    def test_connection_error_becomes_notification_error(self, notifier, http_client):
        http_client.post.side_effect = ConnectionError("connection refused")

        with pytest.raises(NotificationError, match="unreachable") as raised:
            notifier.send_email("ana@example.com", "Hello", "Body")
        assert isinstance(raised.value.__cause__, ConnectionError)

    def test_http_error_status_becomes_notification_error(self, notifier, http_client):
        http_client.post.return_value.status_code = 503

        with pytest.raises(NotificationError, match="HTTP 503"):
            notifier.send_sms("+523312345678", "Hello")

    @pytest.mark.parametrize("recipient", ["", "no-at-sign", "two@@example.com", None])
    def test_invalid_email_is_rejected_before_calling_gateway(self, notifier, http_client, recipient):
        with pytest.raises(ValueError, match="Invalid email"):
            notifier.send_email(recipient, "Hello", "Body")
        http_client.post.assert_not_called()

    @pytest.mark.parametrize("phone", ["3312345678", "+12", "+52-33-1234", None])
    def test_invalid_phone_is_rejected_before_calling_gateway(self, notifier, http_client, phone):
        with pytest.raises(ValueError, match="Invalid phone"):
            notifier.send_sms(phone, "Hello")
        http_client.post.assert_not_called()


class TestRepositoryWithMockedDatabase:
    @pytest.fixture(name="database")
    def fixture_database(self):
        return Mock(spec=Database)

    def test_save_new_task_inserts_and_assigns_generated_id(self, database):
        database.insert.return_value = 42
        task = Task("Persist me")

        TaskRepository(database).save(task)

        assert task.id == 42
        database.insert.assert_called_once_with(task)
        database.update.assert_not_called()

    def test_database_failure_becomes_repository_error_and_is_logged(self, database, caplog):
        database.get_all.side_effect = DatabaseError("connection lost")

        with caplog.at_level(logging.ERROR), pytest.raises(RepositoryError, match="'get_all' failed"):
            TaskRepository(database).find_all()
        assert "connection lost" in caplog.text


class TestServiceErrorScenarios:
    def test_repository_failure_handled_gracefully(self, service, mock_repository, mock_notifier):
        mock_repository.save.side_effect = RepositoryError("Database operation 'insert' failed")

        with pytest.raises(RepositoryError, match="insert"):
            service.create_task("Test Task")

        mock_notifier.send_email.assert_not_called()

    def test_notification_failure_does_not_break_workflow(self, service, mock_repository, mock_notifier, caplog):
        mock_notifier.send_email.side_effect = NotificationError("SMTP server unavailable")

        with caplog.at_level(logging.WARNING):
            task = service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once_with(task)
        mock_notifier.send_email.assert_called_once()
        assert "SMTP server unavailable" in caplog.text

    def test_sms_failure_does_not_block_status_update(self, service, mock_repository, mock_notifier):
        task = Task("Hotfix", priority=TaskPriority.URGENT)
        mock_repository.find_by_id.return_value = task
        mock_notifier.send_sms.side_effect = NotificationError("SMS quota exceeded")

        service.update_task_status(7, TaskStatus.IN_PROGRESS)

        assert task.status is TaskStatus.IN_PROGRESS
        mock_notifier.send_email.assert_called_once_with("user@example.com", "Task Status Updated", ANY)

    def test_one_failed_overdue_notification_does_not_stop_the_rest(
        self, service, mock_repository, mock_notifier, clock
    ):
        first, second = Task("Report A", due_date=clock.in_days(1)), Task("Report B", due_date=clock.in_days(1))
        mock_repository.find_all.return_value = [first, second]
        mock_notifier.send_email.side_effect = [NotificationError("timeout"), "msg-2"]
        clock.advance(days=3)

        assert service.check_overdue_tasks() == [first, second]
        assert mock_notifier.send_email.call_count == 2

    def test_programming_errors_from_notifier_are_not_swallowed(self, service, mock_notifier):
        """Only delivery failures are tolerated; a misconfigured recipient must surface, not hide."""
        mock_notifier.send_email.side_effect = ValueError("Invalid email address")

        with pytest.raises(ValueError, match="Invalid email address"):
            service.create_task("Misconfigured")

    def test_task_is_saved_before_notification_is_sent(self, service, mock_repository, mock_notifier):
        calls = Mock()
        calls.attach_mock(mock_repository.find_by_title, "find_by_title")
        calls.attach_mock(mock_repository.save, "save")
        calls.attach_mock(mock_notifier.send_email, "send_email")

        task = service.create_task("Ordered task")

        assert calls.mock_calls == [
            call.find_by_title("Ordered task"),
            call.save(task),
            call.send_email("user@example.com", "New Task Created", "Task 'Ordered task' has been created"),
        ]


class TestTimeIsolation:
    def test_clock_can_be_patched_with_unittest_mock(self):
        moment = datetime(2030, 1, 1, 8, 0)
        with patch("task.current_time", return_value=moment) as fake_now:
            task = Task("Patched clock")

        assert task.created_at == moment
        fake_now.assert_called()

    def test_frozen_clock_makes_time_travel_deterministic(self, clock):
        task = Task("Due tomorrow", due_date=clock.in_days(1))
        assert task.is_overdue() is False

        clock.advance(days=1, seconds=1)

        assert task.is_overdue() is True
