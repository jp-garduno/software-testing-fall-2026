"""Test doubles in action: mocks verify behaviour, stubs feed data, fakes simulate state.

Also covers the error scenarios that only test doubles can produce on demand:
database outages and failing email/SMS providers.
"""

import logging
from datetime import timedelta
from unittest.mock import ANY, Mock, call

import pytest

from conftest import NOW, RECIPIENT
from notification_service import NotificationError, NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskRepository
from task_service import ServiceUnavailableError, TaskNotFoundError, TaskService


class TestRepositoryFailures:

    def test_repository_failure_handled_gracefully(self, task_service, mock_repository, mock_notification_service):
        mock_repository.save.side_effect = RepositoryError("Database connection failed")

        with pytest.raises(ServiceUnavailableError, match="Database connection failed"):
            task_service.create_task("Test Task")

        mock_notification_service.send_email.assert_not_called()

    def test_lookup_failure_during_duplicate_check_stops_creation(self, task_service, mock_repository):
        mock_repository.find_by_title.side_effect = RepositoryError("timeout")

        with pytest.raises(ServiceUnavailableError):
            task_service.create_task("Test Task")

        mock_repository.save.assert_not_called()

    def test_failure_saving_status_change_sends_no_notification(self, task_service, mock_repository,
                                                                mock_notification_service):
        mock_repository.find_by_id.return_value = Task("Stored task", now=NOW)
        mock_repository.save.side_effect = RepositoryError("disk full")

        with pytest.raises(ServiceUnavailableError, match="disk full"):
            task_service.update_task_status("id", TaskStatus.IN_PROGRESS)

        mock_notification_service.send_email.assert_not_called()

    def test_failure_during_overdue_check_is_reported(self, task_service, mock_repository):
        mock_repository.find_all.side_effect = RepositoryError("connection reset")

        with pytest.raises(ServiceUnavailableError, match="connection reset"):
            task_service.check_overdue_tasks()

    def test_unexpected_errors_are_not_swallowed(self, task_service, mock_repository):
        """Only RepositoryError is translated; programming errors must surface as-is."""
        mock_repository.find_by_id.side_effect = TypeError("bug")

        with pytest.raises(TypeError, match="bug"):
            task_service.get_task("id")


class TestNotificationFailures:

    def test_notification_failure_does_not_break_workflow(self, task_service, mock_repository,
                                                          mock_notification_service):
        mock_notification_service.send_email.side_effect = NotificationError("SMTP server unavailable")

        task = task_service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        assert task_service.failed_notifications == [("email", "New Task Created", "SMTP server unavailable")]

    def test_notification_failure_is_logged(self, task_service, mock_notification_service, caplog):
        mock_notification_service.send_email.side_effect = NotificationError("SMTP down")

        with caplog.at_level(logging.WARNING, logger="task_service"):
            task_service.create_task("Logged task")

        assert "email notification 'New Task Created' failed: SMTP down" in caplog.text

    def test_sms_failure_still_sends_email(self, task_service, mock_notification_service):
        mock_notification_service.send_sms.side_effect = NotificationError("carrier rejected")

        task_service.create_task("Urgent fix", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        assert task_service.failed_notifications == [("sms", "New Task Created", "carrier rejected")]

    def test_one_failed_overdue_notification_does_not_stop_the_rest(self, task_service, mock_repository,
                                                                    mock_notification_service):
        tasks = [Task(f"Overdue {n}", now=NOW) for n in range(3)]
        for task in tasks:
            task.due_date = NOW - timedelta(days=1)
        mock_repository.find_all.return_value = tasks
        mock_notification_service.send_email.side_effect = [None, NotificationError("rate limited"), None]

        assert task_service.check_overdue_tasks() == tasks
        assert mock_notification_service.send_email.call_count == 3
        assert len(task_service.failed_notifications) == 1


class TestMockInteractions:

    def test_save_happens_before_notification(self, mock_repository, mock_notification_service, task_service):
        manager = Mock()
        manager.attach_mock(mock_repository.save, "save")
        manager.attach_mock(mock_notification_service.send_email, "send_email")

        task = task_service.create_task("Ordered task")

        assert manager.mock_calls == [
            call.save(task),
            call.send_email(RECIPIENT.email, "New Task Created", ANY),
        ]

    def test_multiple_notification_channels_for_urgent_task(self, task_service, mock_notification_service):
        task_service.create_task("Urgent Task", priority=TaskPriority.URGENT)

        assert mock_notification_service.send_email.called
        assert mock_notification_service.send_sms.called

    def test_no_sms_without_phone_number(self, mock_repository, mock_notification_service):
        # The default Recipient has an email address but no phone.
        service = TaskService(mock_repository, mock_notification_service, clock=lambda: NOW)

        service.create_task("Urgent Task", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_not_called()

    def test_spec_mock_rejects_methods_the_real_repository_lacks(self, mock_repository):
        with pytest.raises(AttributeError):
            mock_repository.drop_table()


class TestFakeRepositoryWorkflows:
    """A fake keeps real state, so multi-step workflows can be checked end to end."""

    def test_full_lifecycle_with_fake_repository(self, fake_backed_service, fake_repository):
        task = fake_backed_service.create_task("Lifecycle task", due_date=NOW + timedelta(days=2))

        fake_backed_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        fake_backed_service.update_task_status(task.id, TaskStatus.DONE)
        fake_backed_service.delete_task(task.id)

        assert fake_repository.find_by_id(task.id).status == TaskStatus.ARCHIVED
        assert fake_backed_service.purge_task(task.id) is True
        with pytest.raises(TaskNotFoundError):
            fake_backed_service.get_task(task.id)

    def test_duplicate_title_detected_through_fake_state(self, fake_backed_service):
        fake_backed_service.create_task("Unique title")

        with pytest.raises(ValueError, match="already exists"):
            fake_backed_service.create_task("Unique title")

    def test_rename_frees_the_old_title(self, fake_backed_service):
        task = fake_backed_service.create_task("Old title")
        fake_backed_service.update_task(task.id, title="New title")

        assert fake_backed_service.create_task("Old title").title == "Old title"

    def test_combined_search_through_fake(self, fake_backed_service):
        report = fake_backed_service.create_task("Weekly report", priority=TaskPriority.HIGH,
                                                 due_date=NOW + timedelta(days=2))
        fake_backed_service.create_task("Weekly sync", priority=TaskPriority.LOW, due_date=NOW + timedelta(days=2))
        fake_backed_service.create_task("Report draft", priority=TaskPriority.HIGH, due_date=NOW + timedelta(days=9))

        result = fake_backed_service.search_tasks(priority=TaskPriority.HIGH, title_contains="REPORT",
                                                  due_before=NOW + timedelta(days=3))

        assert result == [report]


class TestRealCollaboratorsWithMockedBoundaries:
    """The real repository and notification service, with only the database and providers mocked."""

    def test_service_with_real_layers(self):
        database = Mock()
        database.values.return_value = []
        email_client, sms_client = Mock(), Mock()

        service = TaskService(TaskRepository(database), NotificationService(email_client, sms_client),
                              RECIPIENT, clock=lambda: NOW)

        task = service.create_task("Layered task", priority=TaskPriority.URGENT)

        database.put.assert_called_once_with(task.id, task)
        email_client.send.assert_called_once_with(
            to=RECIPIENT.email, subject="New Task Created", body="Task 'Layered task' has been created"
        )
        sms_client.send.assert_called_once_with(to=RECIPIENT.phone, message="Task 'Layered task' has been created")

    def test_database_outage_surfaces_as_service_error(self):
        database = Mock()
        database.values.side_effect = ConnectionError("db offline")

        service = TaskService(TaskRepository(database), Mock(spec=NotificationService), clock=lambda: NOW)

        with pytest.raises(ServiceUnavailableError, match="db offline"):
            service.create_task("Any task")
