"""Repository and service boundary cases that exercise conditional paths."""

# pylint: disable=import-error

import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock

from src.notification_service import NotificationError, NotificationService
from src.task import Task, TaskPriority, TaskStatus
from src.task_repository import DuplicateTaskError, TaskRepository
from src.task_service import InvalidTaskTransitionError, TaskService


class TaskRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = TaskRepository()

    def test_save_assigns_ids_and_find_methods_return_saved_task(self) -> None:
        task = self.repository.save(Task("Repository task"))

        self.assertEqual(task.id, 1)
        self.assertIs(self.repository.find_by_id(1), task)
        self.assertIs(self.repository.find_by_title("Repository task"), task)
        self.assertIsNone(self.repository.find_by_title("missing"))

    def test_save_rejects_non_task_values(self) -> None:
        with self.assertRaisesRegex(TypeError, "Task instances"):
            self.repository.save("not a task")  # type: ignore[arg-type]

    def test_save_rejects_duplicate_title_and_identifier(self) -> None:
        self.repository.save(Task("Same title"))
        with self.assertRaises(DuplicateTaskError):
            self.repository.save(Task("Same title"))

        another = Task("Different title")
        another.id = 1
        with self.assertRaisesRegex(DuplicateTaskError, "ID 1"):
            self.repository.save(another)

    def test_find_all_is_ordered_by_identifier(self) -> None:
        first = self.repository.save(Task("First task"))
        second = self.repository.save(Task("Second task"))

        self.assertEqual(self.repository.find_all(), [first, second])

    def test_delete_removes_existing_task_and_reports_missing_task(self) -> None:
        task = self.repository.save(Task("Delete me"))

        self.assertTrue(self.repository.delete(task.id))
        self.assertFalse(self.repository.delete(task.id))
        self.assertIsNone(self.repository.find_by_id(task.id))

    def test_search_combines_status_priority_range_and_partial_title(self) -> None:
        start = datetime.now() + timedelta(days=1)
        matching = Task("Release plan", priority=TaskPriority.HIGH, due_date=start)
        matching.status = TaskStatus.IN_PROGRESS
        self.repository.save(matching)
        self.repository.save(
            Task(
                "Other plan",
                priority=TaskPriority.HIGH,
                due_date=start + timedelta(days=1),
            )
        )
        self.repository.save(Task("Release without date", priority=TaskPriority.HIGH))

        result = self.repository.search(
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            due_after=start,
            due_before=start,
            title="RELEASE",
        )

        self.assertEqual(result, [matching])

    def test_search_rejects_invalid_filter_types_and_ranges(self) -> None:
        now = datetime.now()
        invalid_filters = (
            {"status": "TODO"},
            {"priority": 5},
            {"due_after": "tomorrow"},
            {"due_before": "tomorrow"},
            {"due_after": now + timedelta(days=1), "due_before": now},
            {"title": 3},
        )
        for filters in invalid_filters:
            with self.subTest(filters=filters):
                with self.assertRaises(ValueError):
                    self.repository.search(**filters)


class TaskServiceEdgeCaseTests(unittest.TestCase):
    def test_archived_task_cannot_be_archived_or_updated_again(self) -> None:
        service = TaskService(TaskRepository(), Mock(spec=NotificationService))
        task = service.create_task("Archive only once")
        service.delete_task(task.id)

        with self.assertRaises(InvalidTaskTransitionError):
            service.delete_task(task.id)

        with self.assertRaises(InvalidTaskTransitionError):
            service.update_task(task.id, priority=TaskPriority.HIGH)

    def test_update_succeeds_for_valid_fields_and_existing_title(self) -> None:
        repository = TaskRepository()
        notifications = Mock(spec=NotificationService)
        service = TaskService(repository, notifications)
        task = service.create_task("Before update")
        new_due_date = datetime.now() + timedelta(days=10)

        updated = service.update_task(
            task.id,
            title="After update",
            description="Updated description",
            priority=TaskPriority.HIGH,
            due_date=new_due_date,
        )
        same_title = service.update_task(task.id, title="After update")

        self.assertIs(updated, task)
        self.assertEqual(same_title.title, "After update")
        self.assertEqual(same_title.description, "Updated description")
        self.assertEqual(same_title.priority, TaskPriority.HIGH)
        self.assertEqual(same_title.due_date, new_due_date)

        description_only = service.update_task(
            task.id, description="Description without title change"
        )
        self.assertEqual(
            description_only.description, "Description without title change"
        )
        self.assertIs(repository.find_by_title("After update"), task)

    def test_update_rejects_empty_unknown_or_invalid_fields(self) -> None:
        service = TaskService(TaskRepository(), Mock(spec=NotificationService))
        task = service.create_task("Valid task")

        for changes in ({}, {"status": TaskStatus.DONE}, {"priority": "urgent"}):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    service.update_task(task.id, **changes)

    def test_update_rejects_fields_with_invalid_types(self) -> None:
        service = TaskService(TaskRepository(), Mock(spec=NotificationService))
        task = service.create_task("Valid task")

        for changes in (
            {"title": 10},
            {"description": None},
            {"due_date": "tomorrow"},
        ):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    service.update_task(task.id, **changes)

    def test_update_rejects_invalid_due_date_and_duplicate_title(self) -> None:
        service = TaskService(TaskRepository(), Mock(spec=NotificationService))
        first = service.create_task("First title")
        service.create_task("Second title")

        with self.assertRaisesRegex(ValueError, "future"):
            service.update_task(first.id, due_date=datetime.now() - timedelta(days=1))
        with self.assertRaises(DuplicateTaskError):
            service.update_task(first.id, title="Second title")

    def test_notification_service_boundaries_report_unconfigured_provider(self) -> None:
        service = NotificationService()

        with self.assertRaisesRegex(NotificationError, "not configured"):
            service.send_email("user@example.com", "Subject", "Body")
        with self.assertRaisesRegex(NotificationError, "not configured"):
            service.send_sms("+10000000000", "Urgent task")


if __name__ == "__main__":
    unittest.main()
