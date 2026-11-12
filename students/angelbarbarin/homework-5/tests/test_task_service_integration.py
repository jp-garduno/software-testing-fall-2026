"""Integration tests: TaskService working with TaskRepository and NotificationService.

Two levels of integration are exercised:

* ``service``            - TaskService with a mocked repository and notifier, to verify
                           how the service orchestrates its collaborators.
* ``integrated_service`` - TaskService + the real TaskRepository on a FakeDatabase, with
                           only the notifier mocked, to verify complete workflows.
"""

from datetime import datetime, timedelta
from unittest.mock import ANY, call

import pytest

from task import InvalidTransitionError, Task, TaskPriority, TaskStatus, TaskValidationError
from task_repository import RepositoryError
from task_service import DuplicateTaskError, TaskNotFoundError, TaskService


class TestCreateTask:
    def test_create_task_success_with_notification(self, service, mock_repository, mock_notifier):
        task = service.create_task("Write tests", "Unit and integration tests", TaskPriority.HIGH)

        assert task.title == "Write tests"
        assert task.status == TaskStatus.TODO
        mock_repository.find_by_title.assert_called_once_with("Write tests")
        mock_repository.save.assert_called_once_with(task)
        mock_notifier.notify_task_created.assert_called_once_with("user@example.com", task)
        mock_notifier.notify_urgent_sms.assert_not_called()

    def test_create_task_with_duplicate_title_fails(self, service, mock_repository, mock_notifier):
        mock_repository.find_by_title.return_value = Task("Existing Task")

        with pytest.raises(DuplicateTaskError, match="already exists"):
            service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notifier.notify_task_created.assert_not_called()

    def test_create_task_with_invalid_title_never_reaches_repository(self, service, mock_repository):
        with pytest.raises(TaskValidationError):
            service.create_task("ab")

        mock_repository.find_by_title.assert_not_called()
        mock_repository.save.assert_not_called()

    def test_create_urgent_task_sends_email_and_sms(self, service, mock_notifier):
        task = service.create_task("Server down", priority=TaskPriority.URGENT)

        mock_notifier.notify_task_created.assert_called_once_with("user@example.com", task)
        mock_notifier.notify_urgent_sms.assert_called_once_with("+523312345678", task)

    def test_create_urgent_task_without_sms_number_sends_only_email(self, mock_repository, mock_notifier):
        service = TaskService(mock_repository, mock_notifier)

        service.create_task("Server down", priority=TaskPriority.URGENT)

        mock_notifier.notify_task_created.assert_called_once()
        mock_notifier.notify_urgent_sms.assert_not_called()

    def test_duplicate_title_is_case_insensitive_with_real_repository(self, integrated_service):
        integrated_service.create_task("Prepare exam")

        with pytest.raises(DuplicateTaskError):
            integrated_service.create_task("  PREPARE EXAM ")


class TestStatusWorkflow:
    def test_update_task_status_triggers_notification(self, service, mock_repository, mock_notifier):
        task = Task("Test Task")
        mock_repository.find_by_id.return_value = task

        updated = service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once_with(task)
        mock_notifier.notify_status_change.assert_called_once_with("user@example.com", task, TaskStatus.TODO)

    def test_complete_workflow_create_update_complete(self, integrated_service, repository, mock_notifier, future):
        task = integrated_service.create_task("Homework 5", due_date=future)
        integrated_service.update_task(task.id, description="White box testing", priority=TaskPriority.HIGH)
        integrated_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        integrated_service.update_task_status(task.id, TaskStatus.DONE)

        stored = repository.find_by_id(task.id)
        assert stored.status == TaskStatus.DONE
        assert stored.priority == TaskPriority.HIGH
        assert stored.description == "White box testing"
        assert [c.args[2] for c in mock_notifier.notify_status_change.call_args_list] == [
            TaskStatus.TODO,
            TaskStatus.IN_PROGRESS,
        ]

    def test_update_task_with_invalid_transition_fails(self, service, mock_repository, mock_notifier):
        task = Task("Test Task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        with pytest.raises(InvalidTransitionError, match="Invalid transition"):
            service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()
        mock_notifier.notify_status_change.assert_not_called()

    def test_update_status_of_missing_task_fails(self, service, mock_notifier):
        with pytest.raises(TaskNotFoundError, match="not found"):
            service.update_task_status("missing", TaskStatus.DONE)
        mock_notifier.notify_status_change.assert_not_called()


class TestUpdateTask:
    def test_update_task_saves_when_something_changed(self, service, mock_repository):
        task = Task("Old title")
        mock_repository.find_by_id.return_value = task

        service.update_task(task.id, title="New title", priority=TaskPriority.MEDIUM)

        assert task.title == "New title"
        mock_repository.find_by_title.assert_called_once_with("New title")
        mock_repository.save.assert_called_once_with(task)

    def test_update_task_without_changes_does_not_save(self, service, mock_repository):
        task = Task("Same title")
        mock_repository.find_by_id.return_value = task

        service.update_task(task.id, title="Same title")

        mock_repository.find_by_title.assert_not_called()
        mock_repository.save.assert_not_called()

    def test_update_task_title_to_existing_title_fails(self, integrated_service):
        integrated_service.create_task("Taken title")
        other = integrated_service.create_task("Other title")

        with pytest.raises(DuplicateTaskError):
            integrated_service.update_task(other.id, title="Taken title")
        assert integrated_service.get_task(other.id).title == "Other title"

    def test_update_task_title_case_only_change_is_allowed(self, integrated_service):
        task = integrated_service.create_task("lowercase title")

        integrated_service.update_task(task.id, title="Lowercase Title")

        assert integrated_service.get_task(task.id).title == "Lowercase Title"

    def test_update_task_with_past_due_date_fails(self, service, mock_repository):
        mock_repository.find_by_id.return_value = Task("Due soon")

        with pytest.raises(TaskValidationError, match="future"):
            service.update_task("id", due_date=datetime.now() - timedelta(days=1))
        mock_repository.save.assert_not_called()

    def test_update_task_rejects_unknown_fields(self, service, mock_repository):
        with pytest.raises(ValueError, match="Cannot update field"):
            service.update_task("id", status=TaskStatus.DONE)
        mock_repository.find_by_id.assert_not_called()

    def test_archive_task_prevents_further_updates(self, integrated_service, mock_notifier):
        task = integrated_service.create_task("Old work")
        integrated_service.delete_task(task.id)

        with pytest.raises(InvalidTransitionError, match="Archived"):
            integrated_service.update_task(task.id, title="Revived work")
        with pytest.raises(InvalidTransitionError):
            integrated_service.update_task_status(task.id, TaskStatus.TODO)
        assert mock_notifier.notify_status_change.call_count == 1


class TestDeleteTask:
    def test_delete_task_marks_as_archived(self, integrated_service, repository):
        task = integrated_service.create_task("Soft delete me")

        integrated_service.delete_task(task.id)

        stored = repository.find_by_id(task.id)
        assert stored is not None
        assert stored.status == TaskStatus.ARCHIVED

    def test_purge_archived_task_removes_it_permanently(self, integrated_service, repository):
        task = integrated_service.create_task("Purge me")
        integrated_service.delete_task(task.id)

        integrated_service.purge_task(task.id)

        assert repository.find_by_id(task.id) is None
        with pytest.raises(TaskNotFoundError):
            integrated_service.get_task(task.id)

    def test_purge_active_task_is_rejected(self, integrated_service, repository):
        task = integrated_service.create_task("Still active")

        with pytest.raises(InvalidTransitionError, match="Only archived"):
            integrated_service.purge_task(task.id)
        assert repository.find_by_id(task.id) is not None

    def test_purge_when_repository_reports_nothing_deleted(self, service, mock_repository):
        task = Task("Vanished")
        task.status = TaskStatus.ARCHIVED
        mock_repository.find_by_id.return_value = task
        mock_repository.delete.return_value = False

        with pytest.raises(TaskNotFoundError):
            service.purge_task(task.id)


class TestOverdueAndSearch:
    def test_overdue_task_detection_triggers_notification(self, service, mock_repository, mock_notifier, now):
        overdue = Task("Overdue task", due_date=now + timedelta(hours=1))
        done = Task("Done task", due_date=now + timedelta(hours=1))
        done.status = TaskStatus.DONE
        on_time = Task("Future task", due_date=now + timedelta(days=3))
        mock_repository.find_all.return_value = [overdue, done, on_time]

        result = service.check_overdue_tasks(now + timedelta(days=1))

        assert result == [overdue]
        mock_notifier.notify_overdue.assert_called_once_with("user@example.com", overdue)

    def test_check_overdue_with_no_tasks_sends_nothing(self, service, mock_notifier):
        assert service.check_overdue_tasks() == []
        mock_notifier.notify_overdue.assert_not_called()

    def test_search_tasks_by_status(self, integrated_service):
        first = integrated_service.create_task("First task")
        integrated_service.create_task("Second task")
        integrated_service.update_task_status(first.id, TaskStatus.IN_PROGRESS)

        result = integrated_service.search_tasks(status=TaskStatus.IN_PROGRESS)

        assert result == [first]

    def test_filter_tasks_by_priority_and_title(self, integrated_service):
        integrated_service.create_task("Fix login bug", priority=TaskPriority.HIGH)
        integrated_service.create_task("Fix typo", priority=TaskPriority.LOW)
        integrated_service.create_task("Plan sprint", priority=TaskPriority.HIGH)

        result = integrated_service.search_tasks(priority=TaskPriority.HIGH, title_contains="fix")

        assert [t.title for t in result] == ["Fix login bug"]

    def test_search_returns_highest_priority_first(self, integrated_service):
        for title, priority in [("Low one", TaskPriority.LOW), ("Urgent one", TaskPriority.URGENT)]:
            integrated_service.create_task(title, priority=priority)

        assert [t.title for t in integrated_service.search_tasks()] == ["Urgent one", "Low one"]


class TestFailureHandling:
    def test_repository_failure_handled_gracefully(self, service, mock_repository, mock_notifier):
        mock_repository.save.side_effect = RepositoryError("Database connection failed")

        with pytest.raises(RepositoryError, match="Database connection failed"):
            service.create_task("Test Task")

        mock_notifier.notify_task_created.assert_not_called()

    def test_notification_failure_does_not_break_workflow(self, service, mock_repository, mock_notifier):
        mock_notifier.notify_task_created.side_effect = Exception("SMTP server unavailable")

        task = service.create_task("Test Task")

        assert task.title == "Test Task"
        mock_repository.save.assert_called_once_with(task)
        mock_notifier.notify_task_created.assert_called_once_with(ANY, task)
        assert service.failed_notifications == 1

    def test_notification_failure_on_overdue_continues_with_next_task(
        self, service, mock_repository, mock_notifier, now
    ):
        first = Task("First overdue", due_date=now + timedelta(hours=1))
        second = Task("Second overdue", due_date=now + timedelta(hours=1))
        mock_repository.find_all.return_value = [first, second]
        mock_notifier.notify_overdue.side_effect = [Exception("timeout"), True]

        result = service.check_overdue_tasks(now + timedelta(days=1))

        assert result == [first, second]
        assert mock_notifier.notify_overdue.call_args_list == [
            call("user@example.com", first),
            call("user@example.com", second),
        ]
        assert service.failed_notifications == 1
