"""Parts 2 & 4: Integration and mocking tests for TaskService (12 tests)."""

from datetime import datetime, timedelta
import pytest

from src.notification_service import NotificationService
from src.task import Task, TaskPriority, TaskStatus
from src.task_repository import TaskRepository


class TestTaskServiceIntegration:
    """Integration and mocking test scenarios for TaskService."""

    def test_create_task_success_with_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 1: Creating task saves to repository and sends notification."""
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task("Write tests", "Unit and integration", TaskPriority.HIGH)

        assert task.title == "Write tests"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        assert "New Task Created" in mock_notification_service.send_email.call_args[0][1]

    def test_create_task_with_duplicate_title_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 2: Cannot create task with duplicate title."""
        mock_repository.find_by_title.return_value = Task("Existing Task")

        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_task_status_triggers_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 3: Status update saves and notifies."""
        task = Task("Test Task")
        mock_repository.find_by_id.return_value = task

        updated = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()

    def test_complete_workflow_todo_to_done(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 4: Complete workflow through multiple status changes."""
        task = Task("Complete workflow task")
        mock_repository.find_by_id.return_value = task

        task = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS

        task = task_service.update_task_status(1, TaskStatus.DONE)
        assert task.status == TaskStatus.DONE
        assert mock_repository.save.call_count == 2
        assert mock_notification_service.send_email.call_count == 2

    def test_archive_task_prevents_further_updates(
        self, task_service, mock_repository
    ):
        """Integration 5: Archived task cannot transition to any other state."""
        task = Task("Archived Task")
        mock_repository.find_by_id.return_value = task

        task_service.delete_task(1)
        assert task.status == TaskStatus.ARCHIVED

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

    def test_overdue_task_detection_triggers_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 6: Overdue check finds tasks and sends notifications."""
        overdue_task = Task("Overdue task")
        overdue_task.due_date = datetime.now() - timedelta(days=1)
        future_task = Task("Future task", due_date=datetime.now() + timedelta(days=1))
        mock_repository.find_all.return_value = [overdue_task, future_task]

        overdue = task_service.check_overdue_tasks()

        assert len(overdue) == 1
        assert overdue[0].title == "Overdue task"
        mock_notification_service.send_email.assert_called_once()

    def test_search_and_filter_tasks(self, task_service, mock_repository):
        """Integration 7: Search and filter tasks by status, priority, and title."""
        t1 = Task("Fix login bug", priority=TaskPriority.URGENT)
        t2 = Task("Update docs", priority=TaskPriority.LOW)
        t2.status = TaskStatus.IN_PROGRESS
        mock_repository.find_all.return_value = [t1, t2]

        by_status = task_service.search_tasks(status=TaskStatus.TODO)
        by_priority = task_service.search_tasks(priority=TaskPriority.URGENT)
        by_title = task_service.search_tasks(title_query="docs")
        all_tasks = task_service.search_tasks()

        assert by_status == [t1]
        assert by_priority == [t1]
        assert by_title == [t2]
        assert len(all_tasks) == 2

    def test_update_task_with_invalid_transition_or_missing_id_fails(
        self, task_service, mock_repository
    ):
        """Integration 8: Reject invalid transition and non-existent task ID."""
        mock_repository.find_by_id.return_value = None
        with pytest.raises(ValueError, match="not found"):
            task_service.update_task_status(99, TaskStatus.IN_PROGRESS)

        done_task = Task("Done Task")
        done_task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = done_task
        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

    def test_repository_failure_handled_gracefully(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 9: Handle repository failure and do not send notification."""
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = RuntimeError("Database connection failed")

        with pytest.raises(RuntimeError, match="Database connection failed"):
            task_service.create_task("Test Task")

        mock_notification_service.send_email.assert_not_called()

    def test_notification_failure_does_not_break_workflow(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 10: Notification failure does not prevent task creation."""
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_email.side_effect = RuntimeError("SMTP error")

        task = task_service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()

    def test_multiple_notification_channels_for_urgent_task(
        self, task_service, mock_repository, mock_notification_service
    ):
        """Integration 11: Both email and SMS are sent for URGENT tasks."""
        mock_repository.find_by_title.return_value = None

        task_service.create_task("Urgent Task", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once()

    def test_unmocked_interfaces_raise_not_implemented(self):
        """Integration 12: Verify base interfaces require mocking in tests."""
        repo = TaskRepository(database=None)
        notifier = NotificationService()

        with pytest.raises(NotImplementedError):
            repo.save(Task("Test"))
        with pytest.raises(NotImplementedError):
            repo.find_by_id(1)
        with pytest.raises(NotImplementedError):
            repo.find_by_title("Test")
        with pytest.raises(NotImplementedError):
            repo.find_all()
        with pytest.raises(NotImplementedError):
            repo.delete(1)
        with pytest.raises(NotImplementedError):
            notifier.send_email("user@example.com", "Subj", "Body")
        with pytest.raises(NotImplementedError):
            notifier.send_sms("+15550001234", "Msg")
