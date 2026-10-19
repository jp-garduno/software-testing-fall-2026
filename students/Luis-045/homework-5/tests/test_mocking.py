"""Verify dependency interactions, controlled failures and stateful workflows."""

from datetime import timedelta
from unittest.mock import Mock

import pytest

from src.notification_service import NotificationError
from src.task import Task, TaskPriority, TaskStatus
from src.task_repository import RepositoryError
from src.task_service import TaskService


@pytest.mark.parametrize("method", ["find_by_title", "save"])
def test_creation_repository_errors_propagate_without_notifications(
    method, service, mock_repository, mock_notification
):
    getattr(mock_repository, method).side_effect = RepositoryError("Storage offline")
    with pytest.raises(RepositoryError, match="Storage offline"):
        service.create_task("Cannot save task")
    mock_notification.send_email.assert_not_called()
    mock_notification.send_sms.assert_not_called()


def test_failed_status_save_preserves_original_state_and_timestamp(
    service, mock_repository, mock_notification, clock, now
):
    original = Task("Original task", clock=clock)
    mock_repository.find_by_id.return_value = original
    mock_repository.save.side_effect = RepositoryError("Write failed")
    clock.return_value = now + timedelta(minutes=1)
    with pytest.raises(RepositoryError, match="Write failed"):
        service.update_task_status(original.id, TaskStatus.IN_PROGRESS)
    assert original.status is TaskStatus.TODO
    assert original.updated_at == now
    mock_notification.send_email.assert_not_called()


def test_failed_field_save_preserves_original_data(service, mock_repository, clock):
    original = Task("Original task", clock=clock)
    mock_repository.find_by_id.return_value = original
    mock_repository.save.side_effect = RepositoryError("Write failed")
    with pytest.raises(RepositoryError):
        service.update_task(original.id, description="Unsaved description")
    assert original.description == ""


def test_failed_lookup_prevents_saves(service, mock_repository, mock_notification):
    mock_repository.find_by_id.side_effect = RepositoryError("Read failed")
    with pytest.raises(RepositoryError, match="Read failed"):
        service.delete_task("missing")
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


@pytest.mark.parametrize("operation", ["search_tasks", "check_overdue_tasks"])
def test_failed_listing_is_not_disguised_as_empty_results(
    operation, service, mock_repository, mock_notification
):
    mock_repository.find_all.side_effect = RepositoryError("Read failed")
    with pytest.raises(RepositoryError, match="Read failed"):
        getattr(service, operation)()
    mock_notification.send_email.assert_not_called()


def test_failed_sms_is_logged_after_successful_persistence(
    mock_repository, mock_notification, clock, caplog
):
    service = TaskService(
        mock_repository, mock_notification, clock=clock, phone_number="+525500000000"
    )
    mock_notification.send_sms.side_effect = NotificationError("SMS unavailable")
    task = service.create_task("Urgent task", priority=TaskPriority.URGENT)
    mock_repository.save.assert_called_once_with(task)
    mock_notification.send_email.assert_called_once()
    mock_notification.send_sms.assert_called_once()
    assert "SMS unavailable" in caplog.text


def test_failed_email_does_not_prevent_sms_on_the_second_channel(
    mock_repository, mock_notification, clock
):
    service = TaskService(
        mock_repository, mock_notification, clock=clock, phone_number="+525500000000"
    )
    mock_notification.send_email.side_effect = NotificationError("Email unavailable")
    task = service.create_task("Urgent task", priority=TaskPriority.URGENT)
    assert task.title == "Urgent task"
    mock_notification.send_sms.assert_called_once_with(
        "+525500000000", "Task 'Urgent task' has been created"
    )


def test_failed_notification_keeps_a_status_change_persisted(
    memory_repository, mock_notification, clock
):
    service = TaskService(memory_repository, mock_notification, clock=clock)
    task = service.create_task("Persisted task")
    mock_notification.send_email.side_effect = NotificationError("Email unavailable")
    updated = service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    assert updated.status is TaskStatus.IN_PROGRESS
    assert memory_repository.find_by_id(task.id).status is TaskStatus.IN_PROGRESS


def test_overdue_notification_failure_does_not_skip_other_tasks(
    service, mock_repository, mock_notification, clock, now
):
    tasks = [
        Task(title, due_date=now + timedelta(hours=1), clock=clock)
        for title in ("First task", "Second task")
    ]
    clock.return_value = now + timedelta(hours=2)
    mock_repository.find_all.return_value = tasks
    mock_notification.send_email.side_effect = [NotificationError("One failure"), None]
    assert service.check_overdue_tasks() == tasks
    assert mock_notification.send_email.call_count == 2


def test_status_update_saves_before_notifying(
    service, mock_repository, mock_notification, clock
):
    task = Task("Ordered calls", clock=clock)
    mock_repository.find_by_id.return_value = task
    calls = Mock()
    calls.attach_mock(mock_repository.save, "save")
    calls.attach_mock(mock_notification.send_email, "email")
    updated = service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    assert [operation[0] for operation in calls.mock_calls] == ["save", "email"]
    assert calls.mock_calls[0].args == (updated,)


def test_fake_repository_checks_uniqueness_across_a_complete_workflow(
    memory_repository, mock_notification, clock
):
    service = TaskService(memory_repository, mock_notification, clock=clock)
    task = service.create_task("Unique task")
    service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    service.update_task_status(task.id, TaskStatus.DONE)
    service.delete_task(task.id)
    with pytest.raises(ValueError, match="already exists"):
        service.create_task("Unique task")
    assert memory_repository.find_by_id(task.id).status is TaskStatus.ARCHIVED


def test_urgent_task_without_a_phone_uses_email_only(service, mock_notification):
    service.create_task("Email only", priority=TaskPriority.URGENT)
    mock_notification.send_email.assert_called_once()
    mock_notification.send_sms.assert_not_called()
