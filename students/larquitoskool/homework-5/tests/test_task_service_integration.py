import pytest
from unittest.mock import Mock, call
from datetime import datetime, timedelta
from task import Task, TaskStatus, TaskPriority
from task_repository import TaskRepository
from notification_service import NotificationService
from task_service import TaskService

class TestTaskServiceIntegration:
    @pytest.fixture
    def mock_repository(self): return Mock(spec=TaskRepository)

    @pytest.fixture
    def mock_notification_service(self): return Mock(spec=NotificationService)

    @pytest.fixture
    def task_service(self, mock_repository, mock_notification_service):
        return TaskService(mock_repository, mock_notification_service)

    def test_create_task_success_with_notification(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None
        task = task_service.create_task("Write tests", priority=TaskPriority.HIGH)
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()

    def test_create_task_with_duplicate_title_fails(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = Task("Existing Task")
        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")
        mock_repository.save.assert_not_called()

    def test_update_task_status_triggers_notification(self, task_service, mock_repository, mock_notification_service):
        task = Task("Test Task")
        mock_repository.find_by_id.return_value = task
        task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        mock_repository.save.assert_called_once()
        mock_notification_service.send_email.assert_called_once()

    def test_update_task_with_invalid_transition_fails(self, task_service, mock_repository, mock_notification_service):
        task = Task("Test Task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task
        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

    def test_check_overdue_tasks_triggers_notifications(self, task_service, mock_repository, mock_notification_service):
        overdue_task = Task("Overdue")
        overdue_task.due_date = datetime.now() - timedelta(days=1)
        mock_repository.find_all.return_value = [overdue_task]
        
        task_service.check_overdue_tasks()
        mock_notification_service.send_email.assert_called_once()