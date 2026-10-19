"""Integration tests: TaskService working with its repository and notification service.

The repository and the notification service are both test doubles (see conftest.py),
so these tests exercise the service's orchestration and business rules in isolation
from any database or external API.
"""

from datetime import timedelta

import pytest

from conftest import NOW, RECIPIENT
from task import InvalidTransitionError, Task, TaskPriority, TaskStatus
from task_repository import TaskQuery
from task_service import ArchivedTaskError, DuplicateTitleError, TaskNotFoundError


def stored_task(mock_repository, title="Stored task", status=TaskStatus.TODO, priority=TaskPriority.LOW):
    """Stub find_by_id to return a task in the given state."""
    task = Task(title, priority=priority, now=NOW)
    task.status = status
    mock_repository.find_by_id.return_value = task
    return task


class TestTaskCreation:

    def test_create_task_success_with_notification(self, task_service, mock_repository, mock_notification_service):
        task = task_service.create_task("Write tests", "Unit and integration tests", TaskPriority.HIGH)

        assert task.title == "Write tests"
        assert task.status == TaskStatus.TODO
        assert task.created_at == NOW
        mock_repository.find_by_title.assert_called_once_with("Write tests")
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once_with(
            RECIPIENT.email, "New Task Created", "Task 'Write tests' has been created"
        )
        mock_notification_service.send_sms.assert_not_called()

    def test_create_task_with_duplicate_title_fails(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_title.return_value = Task("Existing Task", now=NOW)

        with pytest.raises(DuplicateTitleError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_invalid_title_is_not_saved(self, task_service, mock_repository,
                                                         mock_notification_service):
        with pytest.raises(ValueError, match="at least 3 characters"):
            task_service.create_task("ab")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_past_due_date_is_not_saved(self, task_service, mock_repository):
        with pytest.raises(ValueError, match="must be in the future"):
            task_service.create_task("Late task", due_date=NOW - timedelta(minutes=1))

        mock_repository.save.assert_not_called()

    def test_create_urgent_task_sends_email_and_sms(self, task_service, mock_notification_service):
        task_service.create_task("Server down", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once_with(
            RECIPIENT.phone, "Task 'Server down' has been created"
        )


class TestStatusUpdates:

    def test_update_task_status_triggers_notification(self, task_service, mock_repository, mock_notification_service):
        task = stored_task(mock_repository)

        updated = task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        assert updated.updated_at == NOW
        mock_repository.find_by_id.assert_called_once_with(task.id)
        mock_repository.save.assert_called_once_with(task)
        subject, body = mock_notification_service.send_email.call_args.args[1:]
        assert subject == "Task Status Updated"
        assert "from TODO to IN_PROGRESS" in body

    def test_complete_workflow_todo_to_done(self, task_service, mock_repository, mock_notification_service):
        task = task_service.create_task("Complete workflow task")
        mock_repository.find_by_id.return_value = task

        task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        task_service.update_task_status(task.id, TaskStatus.DONE)

        assert task.status == TaskStatus.DONE
        assert mock_repository.save.call_count == 3
        subjects = [call.args[1] for call in mock_notification_service.send_email.call_args_list]
        assert subjects == ["New Task Created", "Task Status Updated", "Task Status Updated"]

    def test_update_task_with_invalid_transition_fails(self, task_service, mock_repository, mock_notification_service):
        stored_task(mock_repository, status=TaskStatus.DONE)

        with pytest.raises(InvalidTransitionError, match="Invalid transition"):
            task_service.update_task_status("any-id", TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_status_of_missing_task_fails(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(TaskNotFoundError, match="missing-id not found"):
            task_service.update_task_status("missing-id", TaskStatus.DONE)

        mock_notification_service.send_email.assert_not_called()

    def test_status_change_of_urgent_task_also_sends_sms(self, task_service, mock_repository,
                                                         mock_notification_service):
        task = stored_task(mock_repository, priority=TaskPriority.URGENT)

        task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        mock_notification_service.send_sms.assert_called_once()


class TestFieldUpdates:

    def test_update_task_fields(self, task_service, mock_repository):
        task = stored_task(mock_repository)
        new_due = NOW + timedelta(days=3)

        task_service.update_task(task.id, title="Renamed task", description="New details",
                                 priority=TaskPriority.HIGH, due_date=new_due)

        assert (task.title, task.description, task.priority, task.due_date) == (
            "Renamed task", "New details", TaskPriority.HIGH, new_due)
        assert task.updated_at == NOW
        mock_repository.save.assert_called_once_with(task)

    def test_update_title_to_existing_title_fails(self, task_service, mock_repository):
        stored_task(mock_repository)
        mock_repository.find_by_title.return_value = Task("Taken title", now=NOW)

        with pytest.raises(DuplicateTitleError):
            task_service.update_task("id", title="Taken title")

        mock_repository.save.assert_not_called()

    def test_update_title_to_its_own_title_is_allowed(self, task_service, mock_repository):
        task = stored_task(mock_repository, title="Same title")
        mock_repository.find_by_title.return_value = task

        task_service.update_task(task.id, title="Same title", priority=TaskPriority.MEDIUM)

        assert task.priority == TaskPriority.MEDIUM
        mock_repository.save.assert_called_once()

    def test_update_due_date_to_past_fails(self, task_service, mock_repository):
        stored_task(mock_repository)

        with pytest.raises(ValueError, match="must be in the future"):
            task_service.update_task("id", due_date=NOW - timedelta(days=1))

        mock_repository.save.assert_not_called()

    def test_archive_task_prevents_further_updates(self, task_service, mock_repository, mock_notification_service):
        task = stored_task(mock_repository)
        task_service.delete_task(task.id)
        mock_repository.save.reset_mock()

        with pytest.raises(ArchivedTaskError, match="cannot be modified"):
            task_service.update_task(task.id, title="Changed after archive")
        with pytest.raises(InvalidTransitionError):
            task_service.update_task_status(task.id, TaskStatus.TODO)

        assert task.title == "Stored task"
        mock_repository.save.assert_not_called()
        assert mock_notification_service.send_email.call_count == 1


class TestDeletion:

    def test_delete_task_marks_as_archived(self, task_service, mock_repository, mock_notification_service):
        task = stored_task(mock_repository, status=TaskStatus.IN_PROGRESS)

        task_service.delete_task(task.id)

        assert task.status == TaskStatus.ARCHIVED
        mock_repository.save.assert_called_once_with(task)
        mock_repository.delete.assert_not_called()
        assert "to ARCHIVED" in mock_notification_service.send_email.call_args.args[2]

    def test_delete_already_archived_task_fails(self, task_service, mock_repository):
        stored_task(mock_repository, status=TaskStatus.ARCHIVED)

        with pytest.raises(ArchivedTaskError, match="already archived"):
            task_service.delete_task("id")

    def test_purge_archived_task_deletes_permanently(self, task_service, mock_repository):
        task = stored_task(mock_repository, status=TaskStatus.ARCHIVED)
        mock_repository.delete.return_value = True

        assert task_service.purge_task(task.id) is True
        mock_repository.delete.assert_called_once_with(task.id)

    def test_purge_active_task_is_rejected(self, task_service, mock_repository):
        stored_task(mock_repository, status=TaskStatus.TODO)

        with pytest.raises(ValueError, match="must be archived"):
            task_service.purge_task("id")

        mock_repository.delete.assert_not_called()


class TestOverdueAndSearch:

    def test_overdue_task_detection_triggers_notification(self, task_service, mock_repository,
                                                          mock_notification_service):
        overdue = Task("Overdue task", due_date=NOW + timedelta(hours=1), now=NOW)
        overdue.due_date = NOW - timedelta(days=1)
        upcoming = Task("Future task", due_date=NOW + timedelta(days=1), now=NOW)
        mock_repository.find_all.return_value = [overdue, upcoming]

        result = task_service.check_overdue_tasks()

        assert result == [overdue]
        mock_notification_service.send_email.assert_called_once_with(
            RECIPIENT.email, "Task Overdue", "Task 'Overdue task' is overdue!"
        )
        mock_notification_service.send_sms.assert_not_called()

    def test_overdue_high_priority_task_also_sends_sms(self, task_service, mock_repository,
                                                       mock_notification_service):
        task = Task("Overdue high", priority=TaskPriority.HIGH, now=NOW)
        task.due_date = NOW - timedelta(hours=1)
        mock_repository.find_all.return_value = [task]

        task_service.check_overdue_tasks()

        mock_notification_service.send_sms.assert_called_once()

    def test_no_overdue_tasks_sends_nothing(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_all.return_value = []

        assert not task_service.check_overdue_tasks()
        mock_notification_service.send_email.assert_not_called()

    def test_search_tasks_by_status(self, task_service, mock_repository):
        expected = [Task("In progress task", now=NOW)]
        mock_repository.search.return_value = expected

        result = task_service.search_tasks(status=TaskStatus.IN_PROGRESS)

        assert result == expected
        mock_repository.search.assert_called_once_with(TaskQuery(status=TaskStatus.IN_PROGRESS))

    def test_filter_tasks_by_priority_and_title(self, task_service, mock_repository):
        task_service.search_tasks(priority=TaskPriority.HIGH, title_contains="report")

        mock_repository.search.assert_called_once_with(
            TaskQuery(priority=TaskPriority.HIGH, title_contains="report")
        )

    def test_list_active_tasks_by_priority_excludes_archived(self, task_service, mock_repository):
        low = Task("Low task", priority=TaskPriority.LOW, now=NOW)
        urgent = Task("Urgent task", priority=TaskPriority.URGENT, now=NOW)
        archived = Task("Archived task", priority=TaskPriority.URGENT, now=NOW)
        archived.status = TaskStatus.ARCHIVED
        mock_repository.find_all.return_value = [low, archived, urgent]

        assert task_service.list_active_tasks_by_priority() == [urgent, low]
