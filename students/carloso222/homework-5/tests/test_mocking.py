"""Part 4 - Mocking & test isolation.

Shows the three kinds of test doubles used in this suite:
* stubs  - ``return_value`` / ``side_effect`` that feed predefined data,
* mocks  - ``assert_called_*`` checks on the interactions,
* fakes  - ``FakeDatabase`` (conftest.py), a small working implementation.
"""

import logging
from unittest.mock import ANY, Mock, create_autospec

import pytest
from conftest import NOW, PHONE

from errors import NotificationError, RepositoryError
from notification_service import NotificationService
from task import TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


class TestErrorScenarios:
    def test_repository_failure_handled_gracefully(self, task_service, mock_repository, mock_notification_service):
        mock_repository.save.side_effect = RepositoryError("Database connection failed")

        with pytest.raises(RepositoryError, match="Database connection failed"):
            task_service.create_task("Test Task")

        mock_notification_service.send_email.assert_not_called()  # nothing announced if not saved

    def test_repository_lookup_failure_stops_creation(self, task_service, mock_repository):
        mock_repository.find_by_title.side_effect = RepositoryError("timeout")
        with pytest.raises(RepositoryError):
            task_service.create_task("Test Task")
        mock_repository.save.assert_not_called()

    def test_notification_failure_does_not_break_workflow(
        self, task_service, mock_repository, mock_notification_service, caplog
    ):
        mock_notification_service.send_email.side_effect = NotificationError("SMTP server unavailable")

        with caplog.at_level(logging.WARNING, logger="task_service"):
            task = task_service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        assert "SMTP server unavailable" in caplog.text

    def test_sms_failure_does_not_break_workflow(self, task_service, mock_repository, mock_notification_service):
        mock_notification_service.send_sms.side_effect = NotificationError("SMS provider down")
        task = task_service.create_task("Urgent", priority=TaskPriority.URGENT)
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()

    def test_unexpected_notification_exception_is_also_contained(
        self, task_service, mock_repository, mock_notification_service, make_task
    ):
        task = make_task()
        mock_repository.find_by_id.return_value = task
        mock_notification_service.send_email.side_effect = RuntimeError("bug in client")

        assert task_service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS).status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)

    def test_status_change_not_persisted_is_not_notified(
        self, task_service, mock_repository, mock_notification_service, make_task
    ):
        mock_repository.find_by_id.return_value = make_task()
        mock_repository.save.side_effect = RepositoryError("disk full")
        with pytest.raises(RepositoryError):
            task_service.update_task_status("id", TaskStatus.IN_PROGRESS)
        mock_notification_service.send_email.assert_not_called()


class TestMockInteractions:
    def test_multiple_notification_channels_for_urgent_tasks(self, task_service, mock_notification_service):
        task_service.create_task("Urgent Task", priority=TaskPriority.URGENT)
        assert mock_notification_service.send_email.called
        assert mock_notification_service.send_sms.called

    def test_no_sms_when_phone_not_configured(self, mock_repository, mock_notification_service):
        service = TaskService(mock_repository, mock_notification_service, clock=lambda: NOW)
        service.create_task("Urgent Task", priority=TaskPriority.URGENT)
        mock_notification_service.send_sms.assert_not_called()

    def test_custom_recipient_is_used(self, mock_repository, mock_notification_service):
        service = TaskService(mock_repository, mock_notification_service, clock=lambda: NOW, recipient="me@iteso.mx")
        service.create_task("My task")
        mock_notification_service.send_email.assert_called_once_with("me@iteso.mx", "New Task Created", ANY)

    def test_save_happens_before_notification(self, mock_repository, mock_notification_service):
        manager = Mock()
        manager.attach_mock(mock_repository, "repository")
        manager.attach_mock(mock_notification_service, "notifier")
        service = TaskService(mock_repository, mock_notification_service, clock=lambda: NOW, phone_number=PHONE)

        service.create_task("Ordered task")

        call_names = [c[0] for c in manager.mock_calls]
        assert call_names == ["repository.find_by_title", "repository.save", "notifier.send_email"]

    def test_clock_is_called_once_per_operation(self, mock_repository, mock_notification_service):
        clock = Mock(return_value=NOW)
        service = TaskService(mock_repository, mock_notification_service, clock=clock)
        service.create_task("Clocked task")
        clock.assert_called_once_with()

    def test_autospec_rejects_calls_that_do_not_match_the_real_signature(self):
        repository = create_autospec(TaskRepository, instance=True)
        with pytest.raises(TypeError):
            repository.save()  # real save() requires a task
        with pytest.raises(AttributeError):
            repository.not_a_real_method  # pylint: disable=pointless-statement

    def test_spec_mock_of_notification_service_matches_real_api(self):
        notifier = create_autospec(NotificationService, instance=True)
        notifier.send_email("a@b.com", "s", "b")
        notifier.send_email.assert_called_once_with("a@b.com", "s", "b")


class TestFakeDatabase:
    def test_fake_keeps_state_within_one_test(self, fake_service, fake_database):
        fake_service.create_task("First")
        fake_service.create_task("Second")
        assert len(fake_database.rows) == 2

    def test_fake_starts_empty_in_every_test(self, fake_database):
        assert not fake_database.rows  # proves tests do not share state
