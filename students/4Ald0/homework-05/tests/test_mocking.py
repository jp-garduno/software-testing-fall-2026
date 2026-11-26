from datetime import timedelta
from unittest.mock import Mock, call

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository


def test_save_happens_before_notification(service, repository, notifications):
    timeline = Mock()
    timeline.attach_mock(repository, "repository")
    timeline.attach_mock(notifications, "notifications")
    task = service.create_task("Call order")
    assert timeline.mock_calls == [
        call.repository.find_by_title("Call order"),
        call.repository.save(task),
        call.notifications.send_email("user@example.com", "New Task Created",
                                      "Task 'Call order' has been created"),
    ]


def test_email_outage_does_not_undo_creation(service, repository, notifications, caplog):
    notifications.send_email.side_effect = RuntimeError("SMTP unavailable")
    task = service.create_task("Saved anyway")
    assert task.status is TaskStatus.TODO
    repository.save.assert_called_once_with(task)
    notifications.send_email.assert_called_once()
    assert "Email notification failed" in caplog.text


@pytest.mark.parametrize("priority,expected", [(TaskPriority.URGENT, 1), (TaskPriority.HIGH, 0)])
def test_sms_creation_channels(priority, expected, service, notifications):
    task = service.create_task_with_sms("Send alerts", priority=priority)
    notifications.send_email.assert_called_once()
    assert notifications.send_sms.call_count == expected
    if expected:
        notifications.send_sms.assert_called_once_with(
            "+15555550100", "Urgent task 'Send alerts' has been created")
    assert task.priority is priority


def test_sms_creation_failure_is_nonfatal(service, repository, notifications, caplog):
    notifications.send_sms.side_effect = RuntimeError("SMS offline")
    task = service.create_task_with_sms("Urgent task", priority=TaskPriority.URGENT)
    repository.save.assert_called_once_with(task)
    assert "SMS notification failed" in caplog.text


def test_email_failure_still_attempts_sms(service, notifications):
    notifications.send_email.side_effect = RuntimeError("Email offline")
    assert service.create_task_with_sms("Urgent task", priority=TaskPriority.URGENT)
    notifications.send_sms.assert_called_once()


@pytest.mark.parametrize("failure", [None, "email", "sms"])
def test_urgent_overdue_alerts(failure, service, repository, notifications, clock):
    task = Task("Urgent overdue", priority=TaskPriority.URGENT, clock=clock)
    task.due_date = clock() - timedelta(seconds=1)
    repository.find_all.return_value = [task]
    if failure:
        getattr(notifications, "send_" + failure).side_effect = RuntimeError("Offline")
    assert service.check_overdue_tasks() == [task]
    notifications.send_email.assert_called_once()
    notifications.send_sms.assert_called_once_with(
        "+15555550100", "Task 'Urgent overdue' is overdue")


def test_status_notification_failure_preserves_saved_transition(persisted_service, notifications):
    task = persisted_service.create_task("Task title")
    notifications.send_email.reset_mock()
    notifications.send_email.side_effect = RuntimeError("API offline")
    updated = persisted_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    assert updated.status is TaskStatus.IN_PROGRESS
    assert persisted_service.repository.find_by_id(task.id).status is TaskStatus.IN_PROGRESS
    notifications.send_email.assert_called_once()


def test_repository_lookup_failure_stops_workflow(service, repository, notifications):
    repository.find_by_title.side_effect = RuntimeError("Connection refused")
    with pytest.raises(RuntimeError, match="Connection refused"):
        service.create_task("Database error")
    repository.save.assert_not_called()
    notifications.send_email.assert_not_called()


def test_real_repository_uses_database_stub(clock):
    database = Mock()
    repository = TaskRepository(database)
    task = Task("Stored task", clock=clock)
    database.find_by_id.return_value = task
    database.find_all.return_value = [task]
    assert repository.save(task) is task
    assert repository.find_by_id(task.id) is task
    assert repository.find_by_title("Stored task") is task
    repository.delete(task.id)
    database.save.assert_called_once_with(task)
    database.find_by_id.assert_called_once_with(task.id)
    database.delete.assert_called_once_with(task.id)


@pytest.mark.parametrize("method,args", [
    ("send_email", ("person@example.com", "Subject", "Message")),
    ("send_sms", ("+15555550100", "Message")),
])
def test_notification_adapter_delegates_and_propagates(method, args):
    transport = Mock()
    notifier = NotificationService(transport)
    getattr(transport, method).return_value = "accepted"
    assert getattr(notifier, method)(*args) == "accepted"
    getattr(transport, method).assert_called_once_with(*args)
    getattr(transport, method).side_effect = RuntimeError("Transport error")
    with pytest.raises(RuntimeError, match="Transport error"):
        getattr(notifier, method)(*args)


def test_no_shared_state_in_new_fixture(repository, notifications):
    assert repository.mock_calls == []
    assert notifications.mock_calls == []
