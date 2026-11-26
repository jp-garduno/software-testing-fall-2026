"""TaskService integration with real Task objects and isolated dependencies."""

from datetime import timedelta
from unittest.mock import Mock

import pytest

from src.notification_service import NotificationError
from src.task import Task, TaskPriority, TaskStatus
from src.task_repository import RepositoryError
from src.task_service import TaskService


def test_create_task_saves_before_sending_a_notification(clock):
    repository = Mock()
    repository.find_by_title.return_value = None
    notification = Mock()
    operations = Mock()
    operations.attach_mock(repository.save, "save")
    operations.attach_mock(notification.send_email, "email")
    service = TaskService(repository, notification, clock=clock)

    task = service.create_task("Write integration tests")

    assert task.status is TaskStatus.TODO
    repository.save.assert_called_once_with(task)
    notification.send_email.assert_called_once_with(
        "user@example.com",
        "New Task Created",
        "Task 'Write integration tests' has been created",
    )
    assert [operation[0] for operation in operations.mock_calls] == ["save", "email"]


def test_duplicate_title_is_rejected_without_saving_or_notifying(clock):
    repository = Mock()
    repository.find_by_title.return_value = Task("Existing task", clock=clock)
    notification = Mock()
    service = TaskService(repository, notification, clock=clock)

    with pytest.raises(ValueError, match="already exists"):
        service.create_task("Existing task")

    repository.save.assert_not_called()
    notification.send_email.assert_not_called()


def test_creation_with_invalid_data_has_no_external_side_effects(
    service, mock_repository, mock_notification
):
    with pytest.raises(ValueError, match="Title"):
        service.create_task("ab")
    mock_repository.find_by_title.assert_not_called()
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


def test_complete_workflow_persists_forward_transitions(
    memory_repository, mock_notification, clock, now
):
    service = TaskService(memory_repository, mock_notification, clock=clock)
    task = service.create_task("Complete workflow")
    clock.return_value = now + timedelta(minutes=1)
    service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    clock.return_value = now + timedelta(minutes=2)
    completed = service.update_task_status(task.id, TaskStatus.DONE)

    assert memory_repository.find_by_id(task.id).status is TaskStatus.DONE
    assert completed.created_at == now
    assert completed.updated_at == clock.return_value
    assert task.status is TaskStatus.TODO
    assert mock_notification.send_email.call_count == 3


def test_status_change_notifies_the_old_and_new_status(
    service, mock_repository, mock_notification, clock
):
    task = Task("State change", clock=clock)
    mock_repository.find_by_id.return_value = task
    changed = service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    assert changed.status is TaskStatus.IN_PROGRESS
    mock_repository.save.assert_called_once_with(changed)
    mock_notification.send_email.assert_called_once_with(
        "user@example.com",
        "Task Status Updated",
        "Task 'State change' changed from TODO to IN_PROGRESS",
    )


def test_backward_transition_does_not_save_or_notify(
    service, mock_repository, mock_notification, clock
):
    task = Task("Completed task", clock=clock)
    task.status = TaskStatus.DONE
    mock_repository.find_by_id.return_value = task
    with pytest.raises(ValueError, match="Invalid transition"):
        service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


def test_unknown_task_cannot_change_status(service, mock_repository, mock_notification):
    with pytest.raises(ValueError, match="not found"):
        service.update_task_status("missing", TaskStatus.IN_PROGRESS)
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


@pytest.mark.parametrize(
    "status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
)
def test_every_nonterminal_state_can_be_archived(
    status, service, mock_repository, clock
):
    task = Task("Archive task", clock=clock)
    task.status = status
    mock_repository.find_by_id.return_value = task
    assert (
        service.update_task_status(task.id, TaskStatus.ARCHIVED).status
        is TaskStatus.ARCHIVED
    )


def test_overdue_check_notifies_only_unfinished_past_due_tasks(
    service, mock_repository, mock_notification, clock, now
):
    overdue = Task("Past due task", due_date=now + timedelta(hours=1), clock=clock)
    future = Task("Future task", due_date=now + timedelta(days=1), clock=clock)
    completed = Task("Completed task", due_date=overdue.due_date, clock=clock)
    completed.status = TaskStatus.DONE
    archived = Task("Archived task", due_date=overdue.due_date, clock=clock)
    archived.status = TaskStatus.ARCHIVED
    clock.return_value = now + timedelta(hours=2)
    mock_repository.find_all.return_value = [overdue, future, completed, archived]

    assert service.check_overdue_tasks() == [overdue]
    mock_notification.send_email.assert_called_once_with(
        "user@example.com", "Task Overdue", "Task 'Past due task' is overdue!"
    )


def test_empty_overdue_check_emits_no_notification(service, mock_notification):
    assert service.check_overdue_tasks() == []
    mock_notification.send_email.assert_not_called()


def test_creation_storage_failure_emits_no_success_notification(
    service, mock_repository, mock_notification
):
    mock_repository.save.side_effect = RepositoryError("Database unavailable")
    with pytest.raises(RepositoryError, match="Database unavailable"):
        service.create_task("Cannot persist")
    mock_notification.send_email.assert_not_called()


def test_email_failure_does_not_undo_a_saved_task(
    service, mock_repository, mock_notification, caplog
):
    mock_notification.send_email.side_effect = NotificationError("SMTP unavailable")
    task = service.create_task("Saved despite email failure")
    mock_repository.save.assert_called_once_with(task)
    mock_notification.send_email.assert_called_once()
    assert "SMTP unavailable" in caplog.text


def test_urgent_creation_notifies_both_configured_channels(
    mock_repository, mock_notification, clock
):
    service = TaskService(
        mock_repository, mock_notification, clock=clock, phone_number="+525500000000"
    )
    task = service.create_task("Urgent task", priority=TaskPriority.URGENT)
    assert task.priority is TaskPriority.URGENT
    mock_notification.send_email.assert_called_once()
    mock_notification.send_sms.assert_called_once_with(
        "+525500000000", "Task 'Urgent task' has been created"
    )


def test_lower_priority_tasks_do_not_trigger_sms(
    mock_repository, mock_notification, clock
):
    service = TaskService(
        mock_repository, mock_notification, clock=clock, phone_number="+525500000000"
    )
    service.create_task("Normal task", priority=TaskPriority.HIGH)
    mock_notification.send_sms.assert_not_called()


def test_field_update_preserves_identity_and_creation_time(
    memory_repository, mock_notification, clock, now
):
    service = TaskService(memory_repository, mock_notification, clock=clock)
    original = service.create_task("Original title")
    clock.return_value = now + timedelta(minutes=1)
    updated = service.update_task(
        original.id,
        title="New title",
        description="New description",
        priority=TaskPriority.HIGH,
        due_date=now + timedelta(days=1),
    )
    stored = memory_repository.find_by_id(original.id)
    assert stored.title == updated.title == "New title"
    assert stored.description == "New description"
    assert stored.priority is TaskPriority.HIGH
    assert stored.due_date == now + timedelta(days=1)
    assert updated.id == original.id
    assert updated.created_at == original.created_at
    assert updated.updated_at == clock.return_value
    assert original.title == "Original title"


def test_updating_title_to_another_tasks_title_is_rejected(
    memory_repository, mock_notification, clock
):
    service = TaskService(memory_repository, mock_notification, clock=clock)
    first = service.create_task("First task")
    service.create_task("Second task")
    with pytest.raises(ValueError, match="already exists"):
        service.update_task(first.id, title="Second task")
    assert memory_repository.find_by_id(first.id).title == "First task"


def test_keeping_the_same_title_is_valid(service, mock_repository, clock):
    original = Task("Same title", clock=clock)
    mock_repository.find_by_id.return_value = original
    updated = service.update_task(
        original.id, title=original.title, description="Changed"
    )
    assert updated.title == original.title
    assert updated.description == "Changed"
    mock_repository.find_by_title.assert_not_called()


def test_soft_delete_archives_instead_of_removing_storage(
    service, mock_repository, clock
):
    original = Task("Soft delete", clock=clock)
    mock_repository.find_by_id.return_value = original
    archived = service.delete_task(original.id)
    assert archived.status is TaskStatus.ARCHIVED
    mock_repository.save.assert_called_once_with(archived)
    mock_repository.delete.assert_not_called()


def test_archived_tasks_cannot_be_edited(
    service, mock_repository, mock_notification, clock
):
    original = Task("Archived task", clock=clock)
    original.status = TaskStatus.ARCHIVED
    mock_repository.find_by_id.return_value = original
    with pytest.raises(ValueError, match="Archived"):
        service.update_task(original.id, description="Should not change")
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


def test_archiving_cannot_be_combined_with_field_changes(
    service, mock_repository, clock
):
    original = Task("Archive only", clock=clock)
    mock_repository.find_by_id.return_value = original
    with pytest.raises(ValueError, match="archiving"):
        service.update_task(
            original.id, status=TaskStatus.ARCHIVED, title="Changed title"
        )
    assert original.title == "Archive only"
    mock_repository.save.assert_not_called()


def test_due_date_can_be_cleared(service, mock_repository, clock, now):
    original = Task("Clear due date", due_date=now + timedelta(days=1), clock=clock)
    mock_repository.find_by_id.return_value = original
    assert service.update_task(original.id, due_date=None).due_date is None


def test_invalid_update_is_atomic(
    service, mock_repository, mock_notification, clock, now
):
    original = Task("Original task", clock=clock)
    mock_repository.find_by_id.return_value = original
    with pytest.raises(ValueError, match="future"):
        service.update_task(original.id, title="Changed title", due_date=now)
    assert original.title == "Original task"
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


def test_unknown_fields_are_rejected(service, mock_repository, clock):
    original = Task("Protected fields", clock=clock)
    mock_repository.find_by_id.return_value = original
    with pytest.raises(ValueError, match="Unknown fields"):
        service.update_task(original.id, id="replacement")
    mock_repository.save.assert_not_called()


def test_empty_update_is_a_read_without_side_effects(
    service, mock_repository, mock_notification, clock
):
    original = Task("No changes", clock=clock)
    mock_repository.find_by_id.return_value = original
    result = service.update_task(original.id)
    assert result == original
    assert result is not original
    mock_repository.save.assert_not_called()
    mock_notification.send_email.assert_not_called()


def test_combined_filters_apply_together_inclusively(
    memory_repository, mock_notification, clock, now
):
    service = TaskService(memory_repository, mock_notification, clock=clock)
    target = service.create_task(
        "Write unit tests", priority=TaskPriority.HIGH, due_date=now + timedelta(days=2)
    )
    other = service.create_task(
        "Write more tests", priority=TaskPriority.HIGH, due_date=now + timedelta(days=2)
    )
    service.update_task_status(target.id, TaskStatus.IN_PROGRESS)
    assert (
        service.search_tasks(
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            title="UNIT",
            start_date=now + timedelta(days=2),
            end_date=now + timedelta(days=2),
        )[0].id
        == target.id
    )
    assert other.id != target.id


@pytest.mark.parametrize("filter_name", ["start_date", "end_date"])
def test_date_filters_exclude_tasks_without_due_dates(
    filter_name, service, mock_repository, clock, now
):
    mock_repository.find_all.return_value = [Task("No due date", clock=clock)]
    assert service.search_tasks(**{filter_name: now}) == []


def test_unfiltered_search_returns_all_tasks(service, mock_repository, clock):
    tasks = [Task("First task", clock=clock), Task("Second task", clock=clock)]
    mock_repository.find_all.return_value = tasks
    assert service.search_tasks() == tasks


def test_date_range_with_start_after_end_is_rejected(service, now, mock_repository):
    with pytest.raises(ValueError, match="range"):
        service.search_tasks(start_date=now + timedelta(days=1), end_date=now)
    mock_repository.find_all.assert_not_called()


@pytest.mark.parametrize(
    "filters", [{"status": "TODO"}, {"priority": "HIGH"}, {"title": 42}]
)
def test_invalid_filter_types_are_rejected(filters, service, mock_repository):
    with pytest.raises(ValueError):
        service.search_tasks(**filters)
    mock_repository.find_all.assert_not_called()
