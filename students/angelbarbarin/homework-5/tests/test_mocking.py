"""Mocking and test-isolation tests.

Shows the three kinds of test double side by side and verifies interactions:
call counts, call arguments, call order, retries driven by ``side_effect`` and
patching the clock. Nothing here touches a real database, mail server or SMS API.
"""

from datetime import datetime, timedelta
from unittest.mock import ANY, MagicMock, Mock, call, patch

import pytest

import task as task_module
from notification_service import NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus, TaskValidationError
from task_repository import RepositoryError, TaskRepository
from task_service import TaskService


class TestStubsVersusMocks:
    def test_stub_return_value_drives_the_found_branch(self, service, mock_repository):
        existing = Task("Stubbed task")
        mock_repository.find_by_id.return_value = existing  # stub: canned data

        assert service.get_task(existing.id) is existing

    def test_mock_verifies_exact_arguments(self, service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Any task")

        service.get_task("abc-123")

        mock_repository.find_by_id.assert_called_once_with("abc-123")  # mock: verify behaviour

    def test_spec_rejects_methods_the_real_class_does_not_have(self, mock_repository):
        with pytest.raises(AttributeError):
            mock_repository.find_by_colour("red")

    def test_fake_database_runs_real_repository_logic(self, fake_db, repository, make_task):
        task = repository.save(make_task("Use a fake"))

        assert fake_db.rows == {task.id: task}
        assert repository.find_by_title("use a FAKE") is task


class TestInteractionOrder:
    def test_save_happens_before_notification(self, mock_repository, mock_notifier):
        manager = MagicMock()
        manager.attach_mock(mock_repository.save, "save")
        manager.attach_mock(mock_notifier.notify_task_created, "notify")
        service = TaskService(mock_repository, mock_notifier)

        task = service.create_task("Ordered task")

        assert manager.mock_calls == [call.save(task), call.notify("user@example.com", task)]

    def test_duplicate_check_happens_before_save(self, mock_repository, mock_notifier):
        manager = MagicMock()
        manager.attach_mock(mock_repository.find_by_title, "find_by_title")
        manager.attach_mock(mock_repository.save, "save")

        TaskService(mock_repository, mock_notifier).create_task("Checked task")

        assert [c[0] for c in manager.mock_calls] == ["find_by_title", "save"]

    def test_custom_recipient_is_used(self, mock_repository, mock_notifier):
        service = TaskService(mock_repository, mock_notifier, recipient="angel@example.com")

        service.create_task("Mine")

        mock_notifier.notify_task_created.assert_called_once_with("angel@example.com", ANY)


class TestRetriesWithSideEffect:
    def test_email_succeeds_after_transient_failures(self, notifier, email_client):
        email_client.send.side_effect = [TimeoutError("1"), TimeoutError("2"), None]

        assert notifier.send_email("user@example.com", "Subject", "Body") is True
        assert email_client.send.call_count == 3

    def test_email_gives_up_after_max_retries(self, notifier, email_client):
        email_client.send.side_effect = ConnectionError("SMTP down")

        with pytest.raises(NotificationError, match="email delivery failed after 3 attempt") as error:
            notifier.send_email("user@example.com", "Subject", "Body")

        assert email_client.send.call_count == 3
        assert isinstance(error.value.__cause__, ConnectionError)

    def test_zero_retries_means_single_attempt(self, email_client, sms_client):
        sms_client.send.side_effect = ConnectionError("gateway down")
        notifier = NotificationService(email_client, sms_client, max_retries=0)

        with pytest.raises(NotificationError, match="SMS delivery failed after 1 attempt"):
            notifier.send_sms("+523312345678", "Hi")
        sms_client.send.assert_called_once()

    def test_real_notifier_failure_is_absorbed_by_service(self, mock_repository, email_client, sms_client):
        email_client.send.side_effect = ConnectionError("SMTP down")
        notifier = NotificationService(email_client, sms_client, max_retries=1)
        service = TaskService(mock_repository, notifier)

        task = service.create_task("Created anyway")

        mock_repository.save.assert_called_once_with(task)
        assert email_client.send.call_count == 2
        assert service.failed_notifications == 1


class TestDatabaseFailuresThroughTheStack:
    def test_database_outage_during_create_surfaces_as_repository_error(self, mock_notifier):
        database = Mock()
        database.values.return_value = []
        database.upsert.side_effect = OSError("disk full")
        service = TaskService(TaskRepository(database), mock_notifier)

        with pytest.raises(RepositoryError, match="disk full"):
            service.create_task("Never stored")
        mock_notifier.notify_task_created.assert_not_called()

    def test_database_outage_during_status_update_sends_no_notification(self, service, mock_repository, mock_notifier):
        mock_repository.find_by_id.return_value = Task("In flight")
        mock_repository.save.side_effect = RepositoryError("timeout")

        with pytest.raises(RepositoryError):
            service.update_task_status("id", TaskStatus.IN_PROGRESS)
        mock_notifier.notify_status_change.assert_not_called()


class TestPatchingTheClock:
    def test_due_date_validation_uses_patched_now(self):
        class FrozenDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                return frozen

        frozen = FrozenDatetime(2030, 1, 1, 12, 0, 0)

        with patch.object(task_module, "datetime", FrozenDatetime):
            task = Task("Frozen clock", due_date=frozen + timedelta(seconds=1))
            with pytest.raises(TaskValidationError, match="future"):
                Task("Frozen clock", due_date=frozen)

        assert task.created_at == frozen

    def test_overdue_check_with_injected_time(self, service, mock_repository, mock_notifier):
        task = Task("Due tomorrow", priority=TaskPriority.HIGH, due_date=datetime.now() + timedelta(days=1))
        mock_repository.find_all.return_value = [task]

        assert not service.check_overdue_tasks(datetime.now())
        assert service.check_overdue_tasks(datetime.now() + timedelta(days=2)) == [task]
        mock_notifier.notify_overdue.assert_called_once_with(ANY, task)
