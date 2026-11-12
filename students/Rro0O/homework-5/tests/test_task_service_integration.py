"""Integration tests: TaskService + Task with mocked repository/notifications."""

# pylint: disable=import-error,redefined-outer-name,unused-argument,too-many-arguments,too-many-positional-arguments

from datetime import datetime, timedelta
from unittest.mock import ANY

import pytest

from task import Task, TaskPriority, TaskStatus


def test_create_task_success_with_notification(
    task_service, mock_repository, mock_notification_service
):
    """Test create task success with notification."""
    task = task_service.create_task("Write tests", "Unit and integration", TaskPriority.HIGH)
    assert task.title == "Write tests"
    assert task.status == TaskStatus.TODO
    mock_repository.save.assert_called_once_with(task)
    mock_notification_service.send_email.assert_called_once_with(
        "user@example.com", "New Task Created", ANY
    )


def test_create_task_with_duplicate_title_fails(
    task_service, mock_repository, mock_notification_service
):
    """Test create task with duplicate title fails."""
    mock_repository.find_by_title.return_value = Task("Existing Task")
    with pytest.raises(ValueError, match="already exists"):
        task_service.create_task("Existing Task")
    mock_repository.save.assert_not_called()
    mock_notification_service.send_email.assert_not_called()


def test_create_task_with_invalid_title_does_not_persist(task_service, mock_repository):
    """Test create task with invalid title does not persist."""
    with pytest.raises(ValueError, match="at least 3"):
        task_service.create_task("ab")
    mock_repository.save.assert_not_called()


def test_update_task_status_triggers_notification(
    task_service, mock_repository, mock_notification_service
):
    """Test update task status triggers notification."""
    mock_repository.find_by_id.return_value = Task("Test Task")
    updated = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
    assert updated.status == TaskStatus.IN_PROGRESS
    mock_repository.save.assert_called_once_with(updated)
    args = mock_notification_service.send_email.call_args[0]
    assert "Status Updated" in args[1]
    assert "TODO" in args[2] and "IN_PROGRESS" in args[2]


def test_complete_workflow_todo_to_done(task_service, mock_repository, mock_notification_service):
    """Test complete workflow todo to done."""
    mock_repository.find_by_id.return_value = Task("Workflow task")
    assert (
        task_service.update_task_status(1, TaskStatus.IN_PROGRESS).status == TaskStatus.IN_PROGRESS
    )
    assert task_service.update_task_status(1, TaskStatus.DONE).status == TaskStatus.DONE
    assert mock_repository.save.call_count == 2
    assert mock_notification_service.send_email.call_count == 2


def test_create_update_complete_full_workflow(
    task_service, mock_repository, mock_notification_service
):
    """Test create update complete full workflow."""
    task = task_service.create_task("Full flow", priority=TaskPriority.MEDIUM)
    mock_repository.find_by_id.return_value = task
    task_service.update_task(1, description="More detail", priority=TaskPriority.HIGH)
    task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
    done = task_service.update_task_status(1, TaskStatus.DONE)
    assert done.status == TaskStatus.DONE
    assert done.priority == TaskPriority.HIGH
    assert done.description == "More detail"
    assert mock_notification_service.send_email.call_count == 3


def test_update_task_with_invalid_transition_fails(
    task_service, mock_repository, mock_notification_service
):
    """Test update task with invalid transition fails."""
    task = Task("Test Task")
    task.status = TaskStatus.DONE
    mock_repository.find_by_id.return_value = task
    with pytest.raises(ValueError, match="Invalid transition"):
        task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
    mock_repository.save.assert_not_called()
    mock_notification_service.send_email.assert_not_called()


def test_update_status_of_missing_task_fails(task_service, mock_repository):
    """Test update status of missing task fails."""
    mock_repository.find_by_id.return_value = None
    with pytest.raises(ValueError, match="not found"):
        task_service.update_task_status(99, TaskStatus.DONE)


def test_archive_task_prevents_further_updates(task_service, mock_repository):
    """Test archive task prevents further updates."""
    task = Task("To archive")
    mock_repository.find_by_id.return_value = task
    task_service.update_task_status(1, TaskStatus.ARCHIVED)
    with pytest.raises(ValueError, match="archived"):
        task_service.update_task(1, description="nope")
    with pytest.raises(ValueError, match="Invalid transition"):
        task_service.update_task_status(1, TaskStatus.TODO)


def test_delete_task_marks_as_archived(task_service, mock_repository):
    """Test delete task marks as archived."""
    task = Task("Soft delete me")
    mock_repository.find_by_id.return_value = task
    assert task_service.delete_task(1).status == TaskStatus.ARCHIVED
    mock_repository.delete.assert_not_called()
    mock_repository.save.assert_called_once_with(task)


def test_overdue_task_detection_triggers_notification(
    task_service, mock_repository, mock_notification_service, past, future
):
    """Test overdue task detection triggers notification."""
    overdue = Task("Overdue task")
    overdue.due_date = past
    upcoming = Task("Future task", due_date=future)
    finished = Task("Finished task")
    finished.due_date = past
    finished.status = TaskStatus.DONE
    mock_repository.find_all.return_value = [overdue, upcoming, finished]
    result = task_service.check_overdue_tasks()
    assert result == [overdue]
    mock_notification_service.send_email.assert_called_once()
    assert "overdue" in mock_notification_service.send_email.call_args[0][2].lower()


def test_check_overdue_with_none_overdue_sends_nothing(
    task_service, mock_repository, mock_notification_service
):
    """Test check overdue with none overdue sends nothing."""
    mock_repository.find_all.return_value = [Task("Nothing due")]
    assert task_service.check_overdue_tasks() == []
    mock_notification_service.send_email.assert_not_called()


@pytest.fixture
def stored_tasks(mock_repository, past, future):
    """Stored tasks."""
    now = datetime.now()
    a = Task("Write report", priority=TaskPriority.HIGH, due_date=now + timedelta(days=2))
    b = Task("Review code", priority=TaskPriority.LOW, due_date=now + timedelta(days=10))
    b.status = TaskStatus.IN_PROGRESS
    c = Task("Write tests", priority=TaskPriority.URGENT)
    mock_repository.find_all.return_value = [a, b, c]
    return a, b, c


def test_search_tasks_by_status(task_service, stored_tasks):
    """Test search tasks by status."""
    _, b, _ = stored_tasks
    assert task_service.search_tasks(status=TaskStatus.IN_PROGRESS) == [b]


def test_filter_tasks_by_priority(task_service, stored_tasks):
    """Test filter tasks by priority."""
    _, _, c = stored_tasks
    assert task_service.search_tasks(priority=TaskPriority.URGENT) == [c]


def test_search_by_title_partial_case_insensitive(task_service, stored_tasks):
    """Test search by title partial case insensitive."""
    a, _, c = stored_tasks
    assert task_service.search_tasks(title_query="WRITE") == [a, c]


def test_filter_by_date_range(task_service, stored_tasks):
    """Test filter by date range."""
    a, b, _ = stored_tasks
    now = datetime.now()
    assert task_service.search_tasks(due_from=now, due_to=now + timedelta(days=5)) == [a]
    assert task_service.search_tasks(due_from=now + timedelta(days=5)) == [b]
    assert task_service.search_tasks(due_to=now + timedelta(days=5)) == [a]


def test_combined_filters(task_service, stored_tasks):
    """Test combined filters."""
    a, _, _ = stored_tasks
    result = task_service.search_tasks(
        status=TaskStatus.TODO, priority=TaskPriority.HIGH, title_query="report"
    )
    assert result == [a]
    assert task_service.search_tasks(status=TaskStatus.DONE, title_query="report") == []


def test_sorted_by_priority(task_service, stored_tasks):
    """Test sorted by priority."""
    a, b, c = stored_tasks
    assert task_service.sorted_by_priority() == [c, a, b]


def test_update_task_fields(task_service, mock_repository, future):
    """Test update task fields."""
    task = Task("Old title")
    mock_repository.find_by_id.return_value = task
    task.updated_at = datetime.now() - timedelta(days=1)
    updated = task_service.update_task(
        1, title="New title", description="d" * 600, priority=TaskPriority.URGENT, due_date=future
    )
    assert updated.title == "New title"
    assert len(updated.description) == 500
    assert updated.priority == TaskPriority.URGENT
    assert updated.due_date == future
    assert datetime.now() - updated.updated_at < timedelta(seconds=5)
    mock_repository.save.assert_called_once_with(task)


def test_update_task_title_must_remain_unique(task_service, mock_repository):
    """Test update task title must remain unique."""
    task = Task("Original")
    mock_repository.find_by_id.return_value = task
    mock_repository.find_by_title.return_value = Task("Taken name")
    with pytest.raises(ValueError, match="already exists"):
        task_service.update_task(1, title="Taken name")
    mock_repository.save.assert_not_called()


def test_update_task_same_title_is_allowed(task_service, mock_repository):
    """Test update task same title is allowed."""
    task = Task("Same title")
    mock_repository.find_by_id.return_value = task
    task_service.update_task(1, title="Same title")
    mock_repository.find_by_title.assert_not_called()


def test_update_task_title_matching_itself_is_allowed(task_service, mock_repository):
    """Test update task title matching itself is allowed."""
    task = Task("Before")
    mock_repository.find_by_id.return_value = task
    mock_repository.find_by_title.return_value = task
    assert task_service.update_task(1, title="After").title == "After"


def test_update_task_rejects_past_due_date_and_bad_title(task_service, mock_repository, past):
    """Test update task rejects past due date and bad title."""
    mock_repository.find_by_id.return_value = Task("Editable")
    with pytest.raises(ValueError, match="future"):
        task_service.update_task(1, due_date=past)
    with pytest.raises(ValueError, match="at least 3"):
        task_service.update_task(1, title="x")
    mock_repository.save.assert_not_called()


def test_update_task_without_changes_keeps_fields(task_service, mock_repository):
    """Test update task without changes keeps fields."""
    task = Task("Untouched", "desc", TaskPriority.MEDIUM)
    mock_repository.find_by_id.return_value = task
    task_service.update_task(1, due_date=None)
    assert (task.title, task.description, task.priority) == (
        "Untouched",
        "desc",
        TaskPriority.MEDIUM,
    )
    assert task.due_date is None
