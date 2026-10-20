"""Edge case tests to maximize branch and statement coverage (Part 3)."""

from datetime import datetime, timedelta
import pytest
from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


class TestBaseInterfacesNotImplemented:
    """Ensure base interface classes correctly raise NotImplementedError when unmocked."""

    def test_task_repository_abstract_methods(self):
        """TaskRepository methods raise NotImplementedError when called directly."""
        repo = TaskRepository(database="dummy_db")
        assert repo.database == "dummy_db"

        task = Task("Dummy Task")
        with pytest.raises(NotImplementedError):
            repo.save(task)
        with pytest.raises(NotImplementedError):
            repo.find_by_id(1)
        with pytest.raises(NotImplementedError):
            repo.find_by_title("Dummy Task")
        with pytest.raises(NotImplementedError):
            repo.find_all()
        with pytest.raises(NotImplementedError):
            repo.delete(1)
        with pytest.raises(NotImplementedError):
            repo.filter_by_status(TaskStatus.TODO)
        with pytest.raises(NotImplementedError):
            repo.filter_by_priority(TaskPriority.LOW)
        with pytest.raises(NotImplementedError):
            repo.search_by_title("Dummy")

    def test_notification_service_abstract_methods(self):
        """NotificationService methods raise NotImplementedError when called directly."""
        notifier = NotificationService()
        with pytest.raises(NotImplementedError):
            notifier.send_email("user@test.com", "Subj", "Body")
        with pytest.raises(NotImplementedError):
            notifier.send_sms("1234567890", "Message")


class TestTaskModelEdgeCases:
    """Edge cases for Task model branches."""

    def test_task_transition_to_archived_from_all_active_states(self):
        """transition_to ARCHIVED succeeds from TODO, IN_PROGRESS, and DONE."""
        for state in [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]:
            t = Task("Archivable Task")
            t.status = state
            assert t.transition_to(TaskStatus.ARCHIVED) is True
            assert t.status == TaskStatus.ARCHIVED

    def test_task_update_partial_fields(self):
        """Update only specific fields (description, priority, due date)."""
        task = Task("Initial Task")
        future = datetime.now() + timedelta(days=4)

        # Description only
        task.update(description="Only desc")
        assert task.description == "Only desc"

        # Priority only
        task.update(priority=TaskPriority.URGENT)
        assert task.priority == TaskPriority.URGENT

        # Due date only
        task.update(due_date=future)
        assert task.due_date == future


class TestTaskServiceEdgeCases:
    """Edge cases in TaskService logic and filters."""

    def test_get_task_delegates_to_repository(self, task_service, mock_repository):
        """get_task calls repository.find_by_id and returns result."""
        task = Task("Find Me", task_id=88)
        mock_repository.find_by_id.return_value = task

        result = task_service.get_task(88)
        assert result == task
        mock_repository.find_by_id.assert_called_with(88)

    def test_search_tasks_by_description_match(self, task_service, mock_repository):
        """Search query matches description text even if title does not."""
        t1 = Task("Alpha", description="Contains keyword inside description")
        t2 = Task("Beta", description="Different text")
        mock_repository.find_all.return_value = [t1, t2]

        results = task_service.search_tasks(query="keyword")
        assert len(results) == 1
        assert results[0].title == "Alpha"

    def test_search_tasks_by_date_range(self, task_service, mock_repository):
        """Search filters correctly by start_date and end_date bounds."""
        now = datetime.now()
        t_early = Task("Early", due_date=now + timedelta(days=2))
        t_mid = Task("Mid", due_date=now + timedelta(days=5))
        t_late = Task("Late", due_date=now + timedelta(days=10))
        t_no_due = Task("No Due Date")

        mock_repository.find_all.return_value = [t_early, t_mid, t_late, t_no_due]

        # start_date filter
        res_start = task_service.search_tasks(start_date=now + timedelta(days=4))
        assert len(res_start) == 2
        assert {t.title for t in res_start} == {"Mid", "Late"}

        # end_date filter
        res_end = task_service.search_tasks(end_date=now + timedelta(days=6))
        assert len(res_end) == 2
        assert {t.title for t in res_end} == {"Early", "Mid"}

        # both start_date and end_date
        res_both = task_service.search_tasks(
            start_date=now + timedelta(days=3), end_date=now + timedelta(days=7)
        )
        assert len(res_both) == 1
        assert res_both[0].title == "Mid"

    def test_check_overdue_tasks_handles_notification_failure_gracefully(
        self, task_service, mock_repository, mock_notification_service
    ):
        """check_overdue_tasks continues even if notification raises an exception."""
        overdue_task = Task("Overdue")
        overdue_task.due_date = datetime.now() - timedelta(days=2)
        mock_repository.find_all.return_value = [overdue_task]
        mock_notification_service.send_email.side_effect = RuntimeError("Email down")

        results = task_service.check_overdue_tasks()
        assert len(results) == 1
        assert results[0].title == "Overdue"

    def test_create_task_with_sms_handles_sms_failure_gracefully(
        self, task_service, mock_repository, mock_notification_service
    ):
        """create_task_with_sms succeeds even if SMS delivery raises an exception."""
        mock_repository.find_by_title.return_value = None
        mock_notification_service.send_sms.side_effect = RuntimeError("SMS provider down")

        task = task_service.create_task_with_sms("SMS Task")
        assert task.title == "SMS Task"

    def test_delete_task_already_archived_skips_resave(
        self, task_service, mock_repository
    ):
        """Soft delete of an already ARCHIVED task does not re-save."""
        task = Task("Already Archived")
        task.status = TaskStatus.ARCHIVED
        mock_repository.find_by_id.return_value = task

        result = task_service.delete_task(1, soft=True)
        assert result.status == TaskStatus.ARCHIVED
        mock_repository.save.assert_not_called()

    def test_update_task_with_identical_title(self, task_service, mock_repository):
        """Updating task with identical title passes title != task.title check."""
        task = Task("Same Title", task_id=5)
        mock_repository.find_by_id.return_value = task

        updated = task_service.update_task(5, title="Same Title")
        assert updated.title == "Same Title"
        mock_repository.save.assert_called_once_with(task)

    def test_src_package_exports(self):
        """Verify package initialization and __all__ exports."""
        import src
        for export_name in src.__all__:
            assert hasattr(src, export_name)

