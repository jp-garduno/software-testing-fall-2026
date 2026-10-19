"""Integration tests for TaskService using isolated dependency mocks."""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


@pytest.fixture
def repository():
    """Return a repository mock constrained by its interface."""
    return Mock(spec=TaskRepository)


@pytest.fixture
def notifications():
    """Return a notification-service mock constrained by its interface."""
    return Mock(spec=NotificationService)


@pytest.fixture
def service(repository, notifications):
    """Create a service with fresh mocked boundaries."""
    return TaskService(repository, notifications)


class TestTaskServiceIntegration:
    """Verify component workflows, mock interactions, and failure behavior."""

    def test_create_task_saves_and_notifies(self, service, repository, notifications):
        """Creation checks uniqueness, persists, and sends a notification."""
        repository.find_by_title.return_value = None
        task = service.create_task("Write tests", priority=TaskPriority.HIGH)
        repository.save.assert_called_once_with(task)
        notifications.send_email.assert_called_once()
        assert "New Task Created" in notifications.send_email.call_args.args[1]

    def test_duplicate_title_does_not_save_or_notify(
        self, service, repository, notifications
    ):
        """Duplicate titles fail before any side effect occurs."""
        repository.find_by_title.return_value = Task("Existing task")
        with pytest.raises(ValueError, match="already exists"):
            service.create_task("Existing task")
        repository.save.assert_not_called()
        notifications.send_email.assert_not_called()

    def test_urgent_task_also_sends_sms(self, service, repository, notifications):
        """Urgent-task creation uses both supported notification channels."""
        repository.find_by_title.return_value = None
        service.create_task("Urgent task", priority=TaskPriority.URGENT)
        notifications.send_email.assert_called_once()
        notifications.send_sms.assert_called_once()

    def test_notification_failure_does_not_break_creation(
        self, service, repository, notifications
    ):
        """Provider failure is isolated from successful persistence."""
        repository.find_by_title.return_value = None
        notifications.send_email.side_effect = ConnectionError("smtp unavailable")
        assert service.create_task("Stable task").title == "Stable task"
        repository.save.assert_called_once()

    def test_repository_failure_prevents_notification(
        self, service, repository, notifications
    ):
        """A save error propagates before the service notifies anyone."""
        repository.find_by_title.return_value = None
        repository.save.side_effect = ConnectionError("database unavailable")
        with pytest.raises(ConnectionError, match="database unavailable"):
            service.create_task("Database task")
        notifications.send_email.assert_not_called()

    def test_status_update_saves_and_notifies(self, service, repository, notifications):
        """A valid state change persists before notifying the user."""
        task = Task("Status task")
        repository.find_by_id.return_value = task
        result = service.update_task_status(7, TaskStatus.IN_PROGRESS)
        assert result.status is TaskStatus.IN_PROGRESS
        repository.save.assert_called_once_with(task)
        assert "TODO to IN_PROGRESS" in notifications.send_email.call_args.args[2]

    def test_complete_workflow_todo_to_done(self, service, repository, notifications):
        """A task proceeds through both forward workflow transitions."""
        task = Task("Workflow task")
        repository.find_by_id.return_value = task
        service.update_task_status(1, TaskStatus.IN_PROGRESS)
        service.update_task_status(1, TaskStatus.DONE)
        assert task.status is TaskStatus.DONE
        assert repository.save.call_count == 2
        assert notifications.send_email.call_count == 2

    def test_missing_or_invalid_status_update_fails(
        self, service, repository, notifications
    ):
        """Not-found and invalid-transition cases do not save or notify."""
        repository.find_by_id.return_value = None
        with pytest.raises(ValueError, match="not found"):
            service.update_task_status(1, TaskStatus.DONE)
        task = Task("Done task")
        task.status = TaskStatus.DONE
        repository.find_by_id.return_value = task
        with pytest.raises(ValueError, match="Invalid transition"):
            service.update_task_status(1, TaskStatus.IN_PROGRESS)
        repository.save.assert_not_called()
        notifications.send_email.assert_not_called()

    def test_update_task_changes_editable_fields(self, service, repository):
        """Editable fields are persisted and long descriptions are bounded."""
        task = Task("Original task")
        repository.find_by_id.return_value = task
        repository.find_by_title.return_value = None
        due = datetime.now() + timedelta(days=2)
        result = service.update_task(
            1,
            title="Updated task",
            description="x" * 600,
            priority=TaskPriority.HIGH,
            due_date=due,
        )
        assert result.title == "Updated task"
        assert len(result.description) == 500
        assert result.priority is TaskPriority.HIGH
        assert result.due_date == due

    def test_archived_task_cannot_be_updated_or_restored(self, service, repository):
        """Archive is a soft delete and a terminal state."""
        task = Task("Archive task")
        repository.find_by_id.return_value = task
        assert service.delete_task(1).status is TaskStatus.ARCHIVED
        with pytest.raises(ValueError, match="Archived tasks"):
            service.update_task(1, title="Other title")

    def test_overdue_check_notifies_only_overdue_tasks(
        self, service, repository, notifications
    ):
        """The overdue workflow notifies once per qualifying task."""
        overdue = Task("Overdue task")
        overdue.due_date = datetime.now() - timedelta(days=1)
        future = Task("Future task", due_date=datetime.now() + timedelta(days=1))
        repository.find_all.return_value = [overdue, future]
        assert service.check_overdue_tasks() == [overdue]
        notifications.send_email.assert_called_once()

    def test_search_combines_status_priority_date_and_title_filters(
        self, service, repository
    ):
        """Search filters can be combined without using a real database."""
        due = datetime.now() + timedelta(days=3)
        matching = Task("Prepare Report", priority=TaskPriority.HIGH, due_date=due)
        matching.status = TaskStatus.IN_PROGRESS
        other = Task("Buy groceries", priority=TaskPriority.LOW, due_date=due)
        repository.find_all.return_value = [matching, other]
        results = service.search_tasks(
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            start_date=datetime.now(),
            end_date=due + timedelta(days=1),
            title="report",
        )
        assert results == [matching]
