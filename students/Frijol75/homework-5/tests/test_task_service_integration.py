"""Integration tests for TaskService and workflows (Part 2)."""

from datetime import datetime, timedelta
import pytest
from task import Task, TaskPriority, TaskStatus
from task_service import TaskService


class TestTaskServiceCreationIntegration:
    """Integration tests for task creation workflow."""

    def test_create_task_success_with_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Creating task saves to repository and sends notification."""
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task(
            "Write tests", "Unit and integration tests", TaskPriority.HIGH
        )

        assert task.title == "Write tests"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        assert "New Task Created" in mock_notification_service.send_email.call_args[0][1]

    def test_create_task_with_duplicate_title_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Cannot create task with duplicate title."""
        existing_task = Task("Existing Task")
        mock_repository.find_by_title.return_value = existing_task

        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()


class TestTaskServiceStatusTransitions:
    """Integration tests for task status management and notifications."""

    def test_update_task_status_triggers_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Status update saves to repository and notifies with old and new status."""
        task = Task("Test Task")
        task.status = TaskStatus.TODO
        mock_repository.find_by_id.return_value = task

        updated_task = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert updated_task.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once()
        mock_notification_service.send_email.assert_called_once()
        call_args = mock_notification_service.send_email.call_args[0]
        assert "Status Updated" in call_args[1]
        assert "TODO" in call_args[2]
        assert "IN_PROGRESS" in call_args[2]

    def test_complete_workflow_todo_to_done(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Complete workflow progression from TODO to IN_PROGRESS to DONE."""
        task = Task("Complete workflow task")
        mock_repository.find_by_id.return_value = task

        task = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS

        task = task_service.update_task_status(1, TaskStatus.DONE)
        assert task.status == TaskStatus.DONE

        assert mock_repository.save.call_count == 2
        assert mock_notification_service.send_email.call_count == 2

    def test_update_task_with_invalid_transition_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Invalid status transition is rejected and not persisted."""
        task = Task("Test Task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_task_status_nonexistent_task_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Updating status of non-existent task raises ValueError."""
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task_status(999, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()


class TestTaskServiceOverdueAndLifecycle:
    """Integration tests for overdue detection and deletion lifecycle."""

    def test_check_overdue_tasks_triggers_notifications(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Overdue check finds overdue tasks and sends notifications."""
        overdue_task = Task("Overdue task")
        overdue_task.due_date = datetime.now() - timedelta(days=1)

        not_overdue_task = Task("Future task", due_date=datetime.now() + timedelta(days=2))

        mock_repository.find_all.return_value = [overdue_task, not_overdue_task]

        overdue_tasks = task_service.check_overdue_tasks()

        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].title == "Overdue task"
        mock_notification_service.send_email.assert_called_once()
        assert "overdue" in mock_notification_service.send_email.call_args[0][2].lower()

    def test_check_overdue_tasks_empty_when_no_tasks_overdue(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Overdue check returns empty list when all tasks are future or done."""
        future_task = Task("Future task", due_date=datetime.now() + timedelta(days=1))
        mock_repository.find_all.return_value = [future_task]

        overdue = task_service.check_overdue_tasks()
        assert overdue == []
        mock_notification_service.send_email.assert_not_called()

    def test_delete_task_soft_marks_as_archived(
        self, task_service, mock_repository
    ):
        """Soft delete changes status to ARCHIVED and saves."""
        task = Task("Task to archive")
        mock_repository.find_by_id.return_value = task

        result = task_service.delete_task(1, soft=True)

        assert result.status == TaskStatus.ARCHIVED
        mock_repository.save.assert_called_once_with(task)

    def test_delete_task_hard_removes_from_repository(
        self, task_service, mock_repository
    ):
        """Hard delete calls repository delete directly."""
        mock_repository.delete.return_value = True

        result = task_service.delete_task(1, soft=False)

        assert result is True
        mock_repository.delete.assert_called_once_with(1)

    def test_delete_task_soft_nonexistent_raises_error(
        self, task_service, mock_repository
    ):
        """Soft delete of non-existent task raises ValueError."""
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.delete_task(404, soft=True)


class TestTaskServiceSearchAndFilter:
    """Integration tests for searching and filtering tasks."""

    def test_search_and_filter_workflows(self, task_service, mock_repository):
        """Test query matching, status filtering, and priority filtering."""
        t1 = Task("Write report", priority=TaskPriority.HIGH)
        t1.status = TaskStatus.TODO

        t2 = Task("Code review", priority=TaskPriority.LOW)
        t2.status = TaskStatus.IN_PROGRESS

        t3 = Task("Write unit tests", priority=TaskPriority.URGENT)
        t3.status = TaskStatus.DONE

        mock_repository.find_all.return_value = [t1, t2, t3]

        # Search by query
        results = task_service.search_tasks(query="Write")
        assert len(results) == 2

        # Filter by status
        results = task_service.search_tasks(status=TaskStatus.IN_PROGRESS)
        assert len(results) == 1
        assert results[0].title == "Code review"

        # Filter by priority
        results = task_service.search_tasks(priority=TaskPriority.HIGH)
        assert len(results) == 1
        assert results[0].title == "Write report"

        # Combined filter
        results = task_service.search_tasks(query="Write", status=TaskStatus.DONE)
        assert len(results) == 1
        assert results[0].title == "Write unit tests"


class TestTaskServiceUpdateDetails:
    """Integration tests for updating task attributes."""

    def test_update_task_details_success(self, task_service, mock_repository):
        """Update title, priority, and description via service."""
        task = Task("Original Title", task_id=1)
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = None

        updated = task_service.update_task(
            1,
            title="Brand New Title",
            description="New description",
            priority=TaskPriority.URGENT,
        )

        assert updated.title == "Brand New Title"
        assert updated.description == "New description"
        assert updated.priority == TaskPriority.URGENT
        mock_repository.save.assert_called_once_with(task)

    def test_update_task_duplicate_title_rejected(self, task_service, mock_repository):
        """Reject title update when another task already has the desired title."""
        task1 = Task("Task One", task_id=1)
        task2 = Task("Task Two", task_id=2)
        mock_repository.find_by_id.return_value = task1
        mock_repository.find_by_title.return_value = task2

        with pytest.raises(ValueError, match="already exists"):
            task_service.update_task(1, title="Task Two")

        mock_repository.save.assert_not_called()

    def test_update_task_not_found_raises_error(self, task_service, mock_repository):
        """Updating details of nonexistent task raises ValueError."""
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task(100, title="Whatever")
