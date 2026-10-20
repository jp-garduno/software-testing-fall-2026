"""Integration tests: TaskService working with its (mocked) collaborators."""

from datetime import datetime, timedelta
from unittest.mock import ANY

import pytest

from task import Task, TaskPriority, TaskStatus


def sent_email(mock_notification_service):
    """Return (recipient, subject, body) of the last email."""
    return mock_notification_service.send_email.call_args[0]


class TestCreateTask:
    def test_create_task_success_with_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        task = task_service.create_task("Write tests", "Unit and integration", TaskPriority.HIGH)

        assert task.title == "Write tests"
        assert task.status == TaskStatus.TODO
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "New Task Created", "Task 'Write tests' has been created"
        )

    def test_create_task_with_duplicate_title_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = Task("Existing Task")

        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_invalid_title_is_never_saved(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_title.return_value = None

        with pytest.raises(ValueError, match="at least 3 characters"):
            task_service.create_task("ab")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_past_due_date_is_rejected(
        self, task_service, mock_repository
    ):
        mock_repository.find_by_title.return_value = None

        with pytest.raises(ValueError, match="in the future"):
            task_service.create_task("Late task", due_date=datetime.now() - timedelta(days=1))

        mock_repository.save.assert_not_called()


class TestStatusWorkflow:
    def test_update_task_status_triggers_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_id.return_value = Task("Test Task")

        updated = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(updated)
        _, subject, body = sent_email(mock_notification_service)
        assert "Status Updated" in subject
        assert "TODO" in body and "IN_PROGRESS" in body

    def test_complete_workflow_todo_to_done(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_id.return_value = Task("Complete workflow task")

        task = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS
        task = task_service.update_task_status(1, TaskStatus.DONE)
        assert task.status == TaskStatus.DONE

        assert mock_repository.save.call_count == 2
        assert mock_notification_service.send_email.call_count == 2

    def test_update_task_with_invalid_transition_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        task = Task("Test Task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        assert task.status == TaskStatus.DONE
        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_status_of_missing_task_fails(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task_status(99, TaskStatus.DONE)

        mock_notification_service.send_email.assert_not_called()


class TestArchiveAndDelete:
    def test_delete_task_marks_as_archived(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_id.return_value = Task("Delete me")

        task = task_service.delete_task(1)

        assert task.status == TaskStatus.ARCHIVED
        mock_repository.save.assert_called_once_with(task)
        mock_repository.delete.assert_not_called()  # soft delete only
        mock_notification_service.send_email.assert_called_once()

    def test_archive_task_prevents_further_updates(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_by_id.return_value = Task("Archive me")
        task_service.delete_task(1)
        mock_repository.save.reset_mock()
        mock_notification_service.send_email.reset_mock()

        with pytest.raises(ValueError, match="Archived tasks cannot be modified"):
            task_service.update_task(1, description="new text")
        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.TODO)

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_archived_task_cannot_be_restored(self, task_service, mock_repository):
        task = Task("Gone for good")
        task.status = TaskStatus.ARCHIVED
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.delete_task(1)


class TestOverdue:
    def test_overdue_task_detection_triggers_notification(
        self, task_service, mock_repository, mock_notification_service
    ):
        overdue = Task("Overdue task")
        overdue.due_date = datetime.now() - timedelta(days=1)
        upcoming = Task("Future task", due_date=datetime.now() + timedelta(days=1))
        finished = Task("Finished task")
        finished.due_date = datetime.now() - timedelta(days=3)
        finished.status = TaskStatus.DONE
        mock_repository.find_all.return_value = [overdue, upcoming, finished]

        result = task_service.check_overdue_tasks()

        assert result == [overdue]
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "Task Overdue", "Task 'Overdue task' is overdue!"
        )

    def test_no_overdue_tasks_sends_nothing(
        self, task_service, mock_repository, mock_notification_service
    ):
        mock_repository.find_all.return_value = [Task("Fine task")]

        assert task_service.check_overdue_tasks() == []
        mock_notification_service.send_email.assert_not_called()


class TestSearchAndFilter:
    def test_search_tasks_by_status(self, task_service, mock_repository):
        in_progress = Task("Working on it")
        in_progress.status = TaskStatus.IN_PROGRESS
        mock_repository.search.return_value = [in_progress]

        result = task_service.search_tasks(status=TaskStatus.IN_PROGRESS)

        assert result == [in_progress]
        mock_repository.search.assert_called_once_with(
            status=TaskStatus.IN_PROGRESS, priority=None, due_from=None,
            due_to=None, title_contains=None,
        )

    def test_filter_tasks_by_priority(self, task_service, mock_repository):
        urgent = Task("Fire drill", priority=TaskPriority.URGENT)
        mock_repository.search.return_value = [urgent]

        assert task_service.search_tasks(priority=TaskPriority.URGENT) == [urgent]
        assert mock_repository.search.call_args.kwargs["priority"] == TaskPriority.URGENT

    def test_combined_filters_are_passed_through(self, task_service, mock_repository):
        start, end = datetime.now(), datetime.now() + timedelta(days=7)
        mock_repository.search.return_value = []

        task_service.search_tasks(
            status=TaskStatus.TODO, priority=TaskPriority.HIGH,
            due_from=start, due_to=end, title_contains="report",
        )

        mock_repository.search.assert_called_once_with(
            status=TaskStatus.TODO, priority=TaskPriority.HIGH,
            due_from=start, due_to=end, title_contains="report",
        )


class TestUpdateTask:
    def test_update_task_changes_fields_and_saves(self, task_service, mock_repository):
        task = Task("Old title", "old", TaskPriority.LOW)
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = None
        new_due = datetime.now() + timedelta(days=3)
        before = task.updated_at

        updated = task_service.update_task(
            1, title="New title", description="new", priority=TaskPriority.HIGH, due_date=new_due
        )

        assert (updated.title, updated.description) == ("New title", "new")
        assert updated.priority == TaskPriority.HIGH
        assert updated.due_date == new_due
        assert updated.updated_at >= before
        mock_repository.save.assert_called_once_with(task)

    def test_update_task_title_must_remain_unique(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Mine")
        mock_repository.find_by_title.return_value = Task("Taken")

        with pytest.raises(ValueError, match="already exists"):
            task_service.update_task(1, title="Taken")

        mock_repository.save.assert_not_called()

    def test_update_task_keeping_same_title_is_allowed(self, task_service, mock_repository):
        task = Task("Same title")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = task  # finds itself

        assert task_service.update_task(1, title="Same title").title == "Same title"

    def test_update_task_rejects_past_due_date_without_partial_changes(
        self, task_service, mock_repository
    ):
        task = Task("Stable title", "stable")
        mock_repository.find_by_id.return_value = task

        with pytest.raises(ValueError, match="in the future"):
            task_service.update_task(
                1, description="changed", due_date=datetime.now() - timedelta(days=1)
            )

        assert task.description == "stable"
        mock_repository.save.assert_not_called()

    def test_update_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            task_service.update_task(5, title="Whatever")


class TestGetTask:
    def test_get_task_returns_task(self, task_service, mock_repository):
        task = Task("Find me")
        mock_repository.find_by_id.return_value = task

        assert task_service.get_task(3) is task
        mock_repository.find_by_id.assert_called_once_with(3)

    def test_get_task_not_found(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="Task 3 not found"):
            task_service.get_task(3)


def test_notifications_use_configured_recipient(mock_repository, mock_notification_service):
    from task_service import TaskService

    service = TaskService(mock_repository, mock_notification_service, recipient_email="boss@corp.com")
    mock_repository.find_by_title.return_value = None

    service.create_task("Custom recipient")

    mock_notification_service.send_email.assert_called_once_with("boss@corp.com", ANY, ANY)
