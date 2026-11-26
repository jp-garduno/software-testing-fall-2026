"""TaskService workflows integrated with the in-memory repository."""

# pylint: disable=import-error

import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock

from src.notification_service import NotificationService
from src.task import TaskPriority, TaskStatus
from src.task_repository import TaskRepository
from src.task_service import InvalidTaskTransitionError, TaskNotFoundError, TaskService


class TaskServiceIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = TaskRepository()
        self.notifications = Mock(spec=NotificationService)
        self.service = TaskService(self.repository, self.notifications)

    def test_create_task_saves_and_sends_notification(self) -> None:
        task = self.service.create_task("Write tests", priority=TaskPriority.HIGH)

        self.assertEqual(task.id, 1)
        self.assertIs(self.repository.find_by_id(task.id), task)
        self.notifications.send_email.assert_called_once()
        self.assertEqual(
            self.notifications.send_email.call_args.args[1], "New Task Created"
        )

    def test_duplicate_title_fails_without_second_notification(self) -> None:
        self.service.create_task("Unique task")

        with self.assertRaisesRegex(ValueError, "already exists"):
            self.service.create_task("Unique task")

        self.assertEqual(len(self.repository.find_all()), 1)
        self.notifications.send_email.assert_called_once()

    def test_status_update_saves_and_triggers_notification(self) -> None:
        task = self.service.create_task("Move task")
        self.notifications.reset_mock()

        updated = self.service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        self.assertEqual(updated.status, TaskStatus.IN_PROGRESS)
        self.assertGreaterEqual(updated.updated_at, updated.created_at)
        self.notifications.send_email.assert_called_once()
        self.assertIn(
            "TODO to IN_PROGRESS", self.notifications.send_email.call_args.args[2]
        )

    def test_complete_workflow_moves_todo_to_done(self) -> None:
        task = self.service.create_task("Complete workflow")

        self.service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        completed = self.service.update_task_status(task.id, TaskStatus.DONE)

        self.assertEqual(completed.status, TaskStatus.DONE)
        self.assertEqual(self.notifications.send_email.call_count, 3)

    def test_archive_prevents_further_field_updates(self) -> None:
        task = self.service.create_task("Archive task")
        self.service.delete_task(task.id)

        with self.assertRaisesRegex(InvalidTaskTransitionError, "Archived"):
            self.service.update_task(task.id, description="Not allowed")

    def test_overdue_tasks_trigger_notifications(self) -> None:
        now = datetime.now()
        overdue = self.service.create_task("Past deadline")
        overdue.due_date = now - timedelta(days=1)
        self.service.create_task("No deadline")
        self.notifications.reset_mock()

        result = self.service.check_overdue_tasks(now)

        self.assertEqual(result, [overdue])
        self.notifications.send_email.assert_called_once()
        self.assertEqual(
            self.notifications.send_email.call_args.args[1], "Task Overdue"
        )

    def test_search_filters_by_status(self) -> None:
        todo = self.service.create_task("Still todo")
        in_progress = self.service.create_task("In progress")
        self.service.update_task_status(in_progress.id, TaskStatus.IN_PROGRESS)

        self.assertEqual(
            self.service.search_tasks(status=TaskStatus.TODO),
            [todo],
        )

    def test_search_filters_by_priority(self) -> None:
        self.service.create_task("Low priority")
        urgent = self.service.create_task(
            "Urgent priority", priority=TaskPriority.URGENT
        )

        self.assertEqual(
            self.service.search_tasks(priority=TaskPriority.URGENT),
            [urgent],
        )

    def test_search_combines_title_and_due_date_filters(self) -> None:
        start = datetime.now() + timedelta(days=1)
        matching = self.service.create_task("Release planning", due_date=start)
        self.service.create_task(
            "Unrelated planning", due_date=start + timedelta(days=1)
        )

        result = self.service.search_tasks(
            due_after=start,
            due_before=start,
            title="RELEASE",
        )

        self.assertEqual(result, [matching])

    def test_invalid_status_transition_does_not_change_task(self) -> None:
        task = self.service.create_task("No backward transition")
        self.service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        self.service.update_task_status(task.id, TaskStatus.DONE)
        self.notifications.reset_mock()

        with self.assertRaises(InvalidTaskTransitionError):
            self.service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        self.assertEqual(task.status, TaskStatus.DONE)
        self.notifications.send_email.assert_not_called()

    def test_delete_task_soft_archives_instead_of_removing(self) -> None:
        task = self.service.create_task("Soft delete")

        archived = self.service.delete_task(task.id)

        self.assertIs(self.repository.find_by_id(task.id), archived)
        self.assertEqual(archived.status, TaskStatus.ARCHIVED)

    def test_missing_task_raises_not_found_error(self) -> None:
        with self.assertRaisesRegex(TaskNotFoundError, "Task 999 not found"):
            self.service.update_task_status(999, TaskStatus.IN_PROGRESS)
