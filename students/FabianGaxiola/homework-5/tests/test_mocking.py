"""Mock-based tests for error handling and component interactions."""

# pylint: disable=import-error

import unittest
from unittest.mock import Mock, call

from src.notification_service import NotificationError, NotificationService
from src.task import Task, TaskPriority
from src.task_repository import DuplicateTaskError, TaskRepository
from src.task_service import TaskService


class TaskServiceMockingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = Mock(spec=TaskRepository)
        self.notifications = Mock(spec=NotificationService)
        self.repository.find_by_title.return_value = None
        self.repository.save.side_effect = lambda task: task
        self.service = TaskService(self.repository, self.notifications)

    def test_repository_failure_propagates_and_prevents_notification(self) -> None:
        self.repository.save.side_effect = RuntimeError("Database connection failed")

        with self.assertRaisesRegex(RuntimeError, "Database connection failed"):
            self.service.create_task("Repository failure")

        self.notifications.send_email.assert_not_called()

    def test_notification_failure_does_not_break_task_creation(self) -> None:
        self.notifications.send_email.side_effect = NotificationError(
            "SMTP server unavailable"
        )

        with self.assertLogs("src.task_service", level="WARNING"):
            task = self.service.create_task("Notification failure")

        self.assertEqual(task.title, "Notification failure")
        self.repository.save.assert_called_once_with(task)
        self.notifications.send_email.assert_called_once()

    def test_urgent_task_attempts_both_notification_channels(self) -> None:
        task = self.service.create_task("Critical task", priority=TaskPriority.URGENT)

        self.assertEqual(task.priority, TaskPriority.URGENT)
        self.notifications.send_email.assert_called_once()
        self.notifications.send_sms.assert_called_once()
        self.assertIn("Critical task", self.notifications.send_sms.call_args.args[1])

    def test_sms_failure_is_logged_without_failing_task_creation(self) -> None:
        self.notifications.send_sms.side_effect = NotificationError(
            "SMS provider unavailable"
        )

        with self.assertLogs("src.task_service", level="WARNING"):
            task = self.service.create_task(
                "Critical SMS task", priority=TaskPriority.URGENT
            )

        self.assertEqual(task.title, "Critical SMS task")
        self.notifications.send_sms.assert_called_once()

    def test_task_is_saved_before_email_notification(self) -> None:
        interactions = Mock()
        interactions.attach_mock(self.repository, "repository")
        interactions.attach_mock(self.notifications, "notifications")

        self.service.create_task("Ordered interaction")

        self.assertEqual(
            interactions.mock_calls,
            [
                call.repository.find_by_title("Ordered interaction"),
                call.repository.save(self.repository.save.call_args.args[0]),
                call.notifications.send_email(
                    "user@example.com",
                    "New Task Created",
                    "Task 'Ordered interaction' has been created",
                ),
            ],
        )

    def test_update_field_validation_occurs_before_repository_save(self) -> None:
        existing = Task("Existing title")
        existing.id = 7
        self.repository.find_by_id.return_value = existing

        with self.assertRaisesRegex(ValueError, "must not exceed 500"):
            self.service.update_task(7, description="x" * 501)

        self.repository.save.assert_not_called()

    def test_duplicate_title_update_is_rejected(self) -> None:
        existing = Task("Original title")
        existing.id = 1
        duplicate = Task("Already used")
        duplicate.id = 2
        self.repository.find_by_id.return_value = existing
        self.repository.find_by_title.return_value = duplicate

        with self.assertRaises(DuplicateTaskError):
            self.service.update_task(1, title="Already used")

        self.repository.save.assert_not_called()
