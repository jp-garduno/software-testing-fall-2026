"""Part 2 - Integration tests: TaskService working with TaskRepository and NotificationService.

Two levels are exercised:
* TaskService + mocked repository + mocked notifications (interaction tests), and
* TaskService + real TaskRepository + fake in-memory database (component integration).
"""

from datetime import timedelta
from unittest.mock import ANY, call, patch

import pytest
from conftest import NEXT_WEEK, NOW, PHONE, TOMORROW

from errors import (
    ArchivedTaskError,
    DuplicateTaskError,
    InvalidTransitionError,
    RepositoryError,
    TaskNotFoundError,
)
from task import TaskPriority, TaskStatus


class TestTaskServiceWithMocks:
    def test_create_task_success_with_notification(self, task_service, mock_repository, mock_notification_service):
        task = task_service.create_task("Write tests", "Unit and integration tests", TaskPriority.HIGH)

        assert task.title == "Write tests"
        assert task.created_at == NOW
        mock_repository.find_by_title.assert_called_once_with("Write tests")
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "New Task Created", "Task 'Write tests' has been created"
        )
        mock_notification_service.send_sms.assert_not_called()

    def test_create_urgent_task_also_sends_sms(self, task_service, mock_notification_service):
        task_service.create_task("Server down", priority=TaskPriority.URGENT)

        mock_notification_service.send_email.assert_called_once()
        mock_notification_service.send_sms.assert_called_once_with(PHONE, "URGENT task created: Server down")

    def test_create_task_with_duplicate_title_fails(
        self, task_service, mock_repository, mock_notification_service, make_task
    ):
        mock_repository.find_by_title.return_value = make_task("Existing Task")

        with pytest.raises(DuplicateTaskError, match="already exists"):
            task_service.create_task("Existing Task")

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_create_task_with_invalid_data_does_not_save(self, task_service, mock_repository):
        with pytest.raises(ValueError, match="future"):
            task_service.create_task("Valid title", due_date=NOW - timedelta(days=1))
        mock_repository.save.assert_not_called()

    def test_update_task_status_triggers_notification(
        self, task_service, mock_repository, mock_notification_service, make_task
    ):
        task = make_task("Test Task")
        mock_repository.find_by_id.return_value = task

        updated = task_service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)

        assert updated.status == TaskStatus.IN_PROGRESS
        mock_repository.find_by_id.assert_called_once_with(task.task_id)
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "Task Status Updated", "Task 'Test Task' changed from TODO to IN_PROGRESS"
        )

    def test_complete_workflow_todo_to_done(self, task_service, mock_repository, mock_notification_service):
        task = task_service.create_task("Complete workflow task")
        mock_repository.find_by_id.return_value = task

        task_service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)
        task_service.update_task_status(task.task_id, TaskStatus.DONE)

        assert task.status == TaskStatus.DONE
        assert mock_repository.save.call_count == 3
        subjects = [c.args[1] for c in mock_notification_service.send_email.call_args_list]
        assert subjects == ["New Task Created", "Task Status Updated", "Task Status Updated"]

    def test_update_task_with_invalid_transition_fails(
        self, task_service, mock_repository, mock_notification_service, make_task
    ):
        task = make_task()
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        with pytest.raises(InvalidTransitionError, match="Invalid transition"):
            task_service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)

        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_status_of_missing_task_fails(self, task_service, mock_repository):
        mock_repository.find_by_id.return_value = None
        with pytest.raises(TaskNotFoundError, match="missing-id not found"):
            task_service.update_task_status("missing-id", TaskStatus.DONE)
        mock_repository.save.assert_not_called()

    def test_delete_task_marks_as_archived(self, task_service, mock_repository, mock_notification_service, make_task):
        task = make_task("Old task")
        mock_repository.find_by_id.return_value = task

        result = task_service.delete_task(task.task_id)

        assert result.status == TaskStatus.ARCHIVED
        mock_repository.save.assert_called_once_with(task)
        mock_repository.delete.assert_not_called()  # soft delete, not a real delete
        assert "to ARCHIVED" in mock_notification_service.send_email.call_args.args[2]

    def test_delete_already_archived_task_fails(self, task_service, mock_repository, make_task):
        task = make_task()
        task.status = TaskStatus.ARCHIVED
        mock_repository.find_by_id.return_value = task
        with pytest.raises(ArchivedTaskError, match="already archived"):
            task_service.delete_task(task.task_id)

    def test_archive_task_prevents_further_updates(self, task_service, mock_repository, make_task):
        task = make_task("Archived soon")
        mock_repository.find_by_id.return_value = task
        task_service.delete_task(task.task_id)
        mock_repository.save.reset_mock()

        with pytest.raises(ArchivedTaskError):
            task_service.update_task(task.task_id, title="New title")
        with pytest.raises(InvalidTransitionError):
            task_service.update_task_status(task.task_id, TaskStatus.TODO)
        mock_repository.save.assert_not_called()


class TestTaskServiceUpdatesAndQueries:
    """Field updates, overdue checks, search and permanent deletion (mocked dependencies)."""

    def test_update_task_fields(self, task_service, mock_repository, make_task):
        task = make_task("Draft")
        mock_repository.find_by_id.return_value = task

        task_service.update_task(task.task_id, title="Final", priority=TaskPriority.MEDIUM, due_date=NEXT_WEEK)

        assert (task.title, task.priority, task.due_date) == ("Final", TaskPriority.MEDIUM, NEXT_WEEK)
        assert task.updated_at == NOW
        mock_repository.find_by_title.assert_called_once_with("Final")
        mock_repository.save.assert_called_once_with(task)

    def test_update_task_title_must_stay_unique(self, task_service, mock_repository, make_task):
        task, other = make_task("Mine"), make_task("Taken")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = other

        with pytest.raises(DuplicateTaskError):
            task_service.update_task(task.task_id, title="Taken")
        assert task.title == "Mine"
        mock_repository.save.assert_not_called()

    def test_update_task_keeping_its_own_title_is_allowed(self, task_service, mock_repository, make_task):
        task = make_task("Same title")
        mock_repository.find_by_id.return_value = task
        mock_repository.find_by_title.return_value = task

        task_service.update_task(task.task_id, title="Same title", description="more details")
        assert task.description == "more details"

    def test_update_description_does_not_check_title(self, task_service, mock_repository, make_task):
        task = make_task()
        mock_repository.find_by_id.return_value = task
        task_service.update_task(task.task_id, description="only description")
        mock_repository.find_by_title.assert_not_called()

    def test_overdue_task_detection_triggers_notification(
        self, task_service, mock_repository, mock_notification_service, make_task
    ):
        overdue = make_task("Overdue task", due_date=NOW + timedelta(seconds=1))
        future = make_task("Future task", due_date=NEXT_WEEK)
        done = make_task("Done task", due_date=NOW + timedelta(seconds=1))
        done.status = TaskStatus.DONE
        mock_repository.find_all.return_value = [overdue, future, done]
        task_service.clock = lambda: NOW + timedelta(hours=1)  # one hour later

        result = task_service.check_overdue_tasks()

        assert result == [overdue]
        mock_notification_service.send_email.assert_called_once_with(
            "user@example.com", "Task Overdue", "Task 'Overdue task' is overdue!"
        )
        mock_notification_service.send_sms.assert_not_called()

    def test_overdue_urgent_task_also_sends_sms(
        self, task_service, mock_repository, mock_notification_service, make_task
    ):
        urgent = make_task("Urgent overdue", priority=TaskPriority.URGENT, due_date=TOMORROW)
        mock_repository.find_all.return_value = [urgent]
        task_service.clock = lambda: TOMORROW + timedelta(days=1)

        assert task_service.check_overdue_tasks() == [urgent]
        mock_notification_service.send_sms.assert_called_once_with(PHONE, "URGENT task overdue: Urgent overdue")

    def test_no_overdue_tasks_sends_nothing(self, task_service, mock_repository, mock_notification_service):
        mock_repository.find_all.return_value = []
        assert task_service.check_overdue_tasks() == []
        mock_notification_service.send_email.assert_not_called()

    def test_search_tasks_by_status(self, task_service, mock_repository, make_task):
        low, urgent = make_task("Low", priority=TaskPriority.LOW), make_task("Urgent", priority=TaskPriority.URGENT)
        mock_repository.search.return_value = [low, urgent]

        result = task_service.search_tasks(status=TaskStatus.TODO)

        mock_repository.search.assert_called_once_with(status=TaskStatus.TODO)
        assert result == [urgent, low]  # sorted by priority

    def test_filter_tasks_by_priority(self, task_service, mock_repository, make_task):
        high = make_task("High", priority=TaskPriority.HIGH)
        mock_repository.search.return_value = [high]
        assert task_service.search_tasks(priority=TaskPriority.HIGH) == [high]
        mock_repository.search.assert_called_once_with(priority=TaskPriority.HIGH)

    def test_list_by_priority(self, task_service, mock_repository, make_task):
        medium, high = make_task("Medium", priority=TaskPriority.MEDIUM), make_task("High", priority=TaskPriority.HIGH)
        mock_repository.find_all.return_value = [medium, high]
        assert task_service.list_by_priority() == [high, medium]

    def test_purge_task_deletes_permanently(self, task_service, mock_repository):
        mock_repository.delete.return_value = True
        task_service.purge_task("abc")
        mock_repository.delete.assert_called_once_with("abc")

    def test_purge_missing_task_fails(self, task_service, mock_repository):
        mock_repository.delete.return_value = False
        with pytest.raises(TaskNotFoundError):
            task_service.purge_task("abc")


class TestTaskServiceWithRealRepository:
    """TaskService + TaskRepository + FakeDatabase working together; only notifications are mocked."""

    def test_full_lifecycle_create_update_complete_archive(self, fake_service, fake_repository):
        task = fake_service.create_task("Lifecycle", due_date=NEXT_WEEK)
        fake_service.update_task(task.task_id, priority=TaskPriority.HIGH)
        fake_service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)
        fake_service.update_task_status(task.task_id, TaskStatus.DONE)
        fake_service.delete_task(task.task_id)

        stored = fake_repository.find_by_id(task.task_id)
        assert stored.status == TaskStatus.ARCHIVED
        assert stored.priority == TaskPriority.HIGH

    def test_duplicate_title_detected_through_real_repository(self, fake_service):
        fake_service.create_task("Unique title")
        with pytest.raises(DuplicateTaskError):
            fake_service.create_task("UNIQUE TITLE")  # case-insensitive

    def test_combined_filters_through_real_repository(self, fake_service):
        fake_service.create_task("Write report", priority=TaskPriority.HIGH, due_date=TOMORROW)
        fake_service.create_task("Write tests", priority=TaskPriority.HIGH, due_date=NEXT_WEEK)
        fake_service.create_task("Read report", priority=TaskPriority.LOW, due_date=TOMORROW)

        result = fake_service.search_tasks(
            priority=TaskPriority.HIGH, title_contains="write", due_from=NOW, due_to=TOMORROW
        )
        assert [t.title for t in result] == ["Write report"]

    def test_purge_removes_task_for_good(self, fake_service, fake_repository):
        task = fake_service.create_task("Temporary")
        fake_service.purge_task(task.task_id)
        assert fake_repository.find_by_id(task.task_id) is None
        with pytest.raises(TaskNotFoundError):
            fake_service.purge_task(task.task_id)

    def test_database_failure_surfaces_as_repository_error(self, fake_service, fake_database):
        with patch.object(fake_database, "put", side_effect=ConnectionError("db down")):
            with pytest.raises(RepositoryError, match="db down"):
                fake_service.create_task("Will fail")
        fake_service.notification_service.send_email.assert_not_called()

    def test_notifications_sent_in_workflow_order(self, fake_service, mock_notification_service):
        task = fake_service.create_task("Ordered", priority=TaskPriority.URGENT)
        fake_service.update_task_status(task.task_id, TaskStatus.IN_PROGRESS)

        assert mock_notification_service.mock_calls == [
            call.send_email("user@example.com", "New Task Created", ANY),
            call.send_sms(PHONE, ANY),
            call.send_email("user@example.com", "Task Status Updated", ANY),
        ]
