"""Mocking tests: error scenarios, test doubles and interaction verification."""

# pylint: disable=import-error,redefined-outer-name,unused-argument,too-many-arguments,too-many-positional-arguments

import logging
from unittest.mock import ANY, Mock

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


class FakeTaskRepository:
    """Fake: simplified in-memory implementation of TaskRepository."""

    def __init__(self):
        """Init."""
        self.tasks = {}
        self._next_id = 1

    def save(self, task):
        """Save."""
        if not hasattr(task, "id"):
            task.id = self._next_id
            self._next_id += 1
        self.tasks[task.id] = task

    def find_by_id(self, task_id):
        """Find by id."""
        return self.tasks.get(task_id)

    def find_by_title(self, title):
        """Find by title."""
        return next((t for t in self.tasks.values() if t.title == title), None)

    def find_all(self):
        """Find all."""
        return list(self.tasks.values())


def test_repository_failure_handled_gracefully(
    task_service, mock_repository, mock_notification_service
):
    """Test repository failure handled gracefully."""
    mock_repository.save.side_effect = Exception("Database connection failed")
    with pytest.raises(Exception, match="Database connection failed"):
        task_service.create_task("Test Task")
    mock_notification_service.send_email.assert_not_called()


def test_repository_lookup_failure_propagates(task_service, mock_repository):
    """Test repository lookup failure propagates."""
    mock_repository.find_by_title.side_effect = ConnectionError("db down")
    with pytest.raises(ConnectionError):
        task_service.create_task("Test Task")
    mock_repository.save.assert_not_called()


def test_notification_failure_does_not_break_workflow(
    task_service, mock_repository, mock_notification_service, caplog
):
    """Test notification failure does not break workflow."""
    mock_notification_service.send_email.side_effect = Exception("SMTP server unavailable")
    with caplog.at_level(logging.WARNING):
        task = task_service.create_task("Test Task")
    assert task.title == "Test Task"
    mock_repository.save.assert_called_once()
    mock_notification_service.send_email.assert_called_once()
    assert "SMTP server unavailable" in caplog.text


def test_notification_failure_on_status_update_keeps_saved_state(
    task_service, mock_repository, mock_notification_service
):
    """Test notification failure on status update keeps saved state."""
    mock_repository.find_by_id.return_value = Task("Status task")
    mock_notification_service.send_email.side_effect = Exception("SMTP down")
    assert (
        task_service.update_task_status(1, TaskStatus.IN_PROGRESS).status == TaskStatus.IN_PROGRESS
    )
    mock_repository.save.assert_called_once()


def test_sms_failure_is_swallowed(task_service, mock_notification_service, caplog):
    """Test sms failure is swallowed."""
    mock_notification_service.send_sms.side_effect = Exception("SMS gateway down")
    with caplog.at_level(logging.WARNING):
        task = task_service.create_task_with_sms("Urgent Task", priority=TaskPriority.URGENT)
    assert task.priority == TaskPriority.URGENT
    assert "SMS gateway down" in caplog.text


def test_multiple_notification_channels(task_service, mock_notification_service):
    """Test multiple notification channels."""
    task_service.create_task_with_sms("Urgent Task", priority=TaskPriority.URGENT)
    mock_notification_service.send_email.assert_called_once()
    mock_notification_service.send_sms.assert_called_once_with(
        ANY, "URGENT task created: Urgent Task"
    )


def test_non_urgent_task_does_not_send_sms(task_service, mock_notification_service):
    """Test non urgent task does not send sms."""
    task_service.create_task_with_sms("Calm Task", priority=TaskPriority.HIGH)
    mock_notification_service.send_sms.assert_not_called()


def test_save_happens_before_notification(task_service, mock_repository, mock_notification_service):
    """Test save happens before notification."""
    manager = Mock()
    manager.attach_mock(mock_repository.save, "save")
    manager.attach_mock(mock_notification_service.send_email, "send_email")
    task = task_service.create_task("Ordered calls")
    assert [c[0] for c in manager.mock_calls] == ["save", "send_email"]
    assert manager.mock_calls[0].args == (task,)


def test_stub_returns_predefined_task(task_service, mock_repository):
    """Test stub returns predefined task."""
    stub = Task("Stubbed")
    mock_repository.find_by_id.return_value = stub
    assert task_service.update_task_status(7, TaskStatus.IN_PROGRESS) is stub
    mock_repository.find_by_id.assert_called_once_with(7)


def test_fake_repository_end_to_end(mock_notification_service):
    """Test fake repository end to end."""
    service = TaskService(FakeTaskRepository(), mock_notification_service)
    task = service.create_task("Fake backed")
    with pytest.raises(ValueError, match="already exists"):
        service.create_task("Fake backed")
    service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    service.delete_task(task.id)
    assert service.repository.find_by_id(task.id).status == TaskStatus.ARCHIVED
    assert mock_notification_service.send_email.call_count == 3


def test_mocks_respect_interface_spec(mock_repository):
    """Test mocks respect interface spec."""
    with pytest.raises(AttributeError):
        mock_repository.nonexistent_method()


def test_real_interfaces_must_be_mocked():
    """Test real interfaces must be mocked."""
    repo = TaskRepository(database=object())
    notifier = NotificationService()
    calls = (
        (repo.save, (None,)),
        (repo.find_by_id, (1,)),
        (repo.find_by_title, ("x",)),
        (repo.find_all, ()),
        (repo.delete, (1,)),
        (notifier.send_email, ("a", "b", "c")),
        (notifier.send_sms, ("1", "m")),
    )
    for method, args in calls:
        with pytest.raises(NotImplementedError):
            method(*args)
