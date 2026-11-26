from unittest.mock import ANY

import pytest

from task import TaskPriority, TaskStatus


class TestMockStubFake:
    def test_stub_returns_predefined_data(self, task_service, mock_repository):
        mock_repository.find_by_title.return_value = None  # stub
        assert task_service.create_task("Stubbed task").title == "Stubbed task"

    def test_mock_verifies_exact_arguments(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task("Verified task")

        mock_repository.find_by_title.assert_called_once_with("Verified task")
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "New Task Created", ANY)

    def test_save_happens_before_notification(
            self, task_service, mock_repository, mock_notification_service):
        events = []
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = lambda t: events.append("save")
        mock_notification_service.send_email.side_effect = lambda *a: events.append("email")

        task_service.create_task("Ordered task")

        assert events == ["save", "email"]

    def test_fake_repository_full_workflow(self, fake_repository, mock_notification_service):
        from task_service import TaskService
        service = TaskService(fake_repository, mock_notification_service)

        created = service.create_task("Fake workflow")
        service.update_task_status(created.id, TaskStatus.IN_PROGRESS)
        service.update_task_status(created.id, TaskStatus.DONE)

        assert fake_repository.find_by_id(created.id).status == TaskStatus.DONE
        assert mock_notification_service.send_email.call_count == 3

    def test_fake_repository_rejects_duplicates(self, fake_repository, mock_notification_service):
        from task_service import TaskService
        service = TaskService(fake_repository, mock_notification_service)
        service.create_task("Unique title")
        with pytest.raises(ValueError, match="already exists"):
            service.create_task("Unique title")


class TestErrorScenarios:
    def test_repository_failure_propagates_and_skips_notification(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None
        mock_repository.save.side_effect = Exception("Database connection failed")

        with pytest.raises(Exception, match="Database connection failed"):
            task_service.create_task("Test Task")

        mock_notification_service.send_email.assert_not_called()

    def test_repository_read_failure_propagates(self, task_service, mock_repository):
        mock_repository.find_all.side_effect = Exception("DB down")
        with pytest.raises(Exception, match="DB down"):
            task_service.check_overdue_tasks()

    def test_notification_failure_does_not_break_workflow(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_email.side_effect = Exception("SMTP server unavailable")

        task = task_service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once()
        mock_notification_service.send_email.assert_called_once()

    def test_sms_failure_does_not_break_urgent_creation(
            self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_sms.side_effect = Exception("SMS gateway down")

        task = task_service.create_task_with_sms("Urgent", priority=TaskPriority.URGENT)

        assert task.priority == TaskPriority.URGENT
        mock_notification_service.send_sms.assert_called_once()

    def test_overdue_notification_failure_still_returns_tasks(
            self, task_service, mock_repository, mock_notification_service, make_task):
        from datetime import datetime, timedelta
        late = make_task("Late", due_date=datetime.now() - timedelta(days=1))
        mock_repository.find_all.return_value = [late]
        mock_notification_service.send_email.side_effect = Exception("boom")

        assert task_service.check_overdue_tasks() == [late]