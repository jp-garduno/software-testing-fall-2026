"""Isolated unit tests for the Task model."""

import unittest
from datetime import datetime, timedelta, timezone

from src.task import Task, TaskPriority, TaskStatus  # pylint: disable=import-error


class TaskCreationTests(unittest.TestCase):
    def test_task_creation_uses_valid_data_and_defaults(self) -> None:
        task = Task("Write tests")

        self.assertEqual(task.title, "Write tests")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(task.priority, TaskPriority.LOW)
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.id)
        self.assertLessEqual(task.created_at, task.updated_at)

    def test_task_creation_accepts_future_due_date_and_optional_fields(self) -> None:
        due_date = datetime.now() + timedelta(days=1)
        task = Task("Plan release", "Prepare the release", TaskPriority.HIGH, due_date)

        self.assertEqual(task.description, "Prepare the release")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertEqual(task.due_date, due_date)

    def test_task_creation_rejects_empty_title(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 3 characters"):
            Task("")

    def test_task_creation_rejects_title_below_minimum_length(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 3 characters"):
            Task("ab")

    def test_task_creation_accepts_title_at_maximum_length(self) -> None:
        self.assertEqual(len(Task("a" * 100).title), 100)

    def test_task_creation_rejects_title_above_maximum_length(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not exceed 100"):
            Task("a" * 101)

    def test_task_creation_rejects_non_string_title(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 3 characters"):
            Task(None)  # type: ignore[arg-type]

    def test_task_creation_accepts_description_at_maximum_length(self) -> None:
        self.assertEqual(len(Task("Valid task", "d" * 500).description), 500)

    def test_task_creation_rejects_description_above_maximum_length(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not exceed 500"):
            Task("Valid task", "d" * 501)

    def test_task_creation_rejects_non_string_description(self) -> None:
        with self.assertRaisesRegex(ValueError, "Description must be a string"):
            Task("Valid task", None)  # type: ignore[arg-type]

    def test_task_creation_rejects_invalid_priority(self) -> None:
        with self.assertRaisesRegex(ValueError, "TaskPriority"):
            Task("Valid task", priority=1)  # type: ignore[arg-type]

    def test_due_date_validation_rejects_past_and_current_dates(self) -> None:
        now = datetime(2030, 1, 1)
        for due_date in (now - timedelta(seconds=1), now):
            with self.subTest(due_date=due_date):
                with self.assertRaisesRegex(ValueError, "future"):
                    Task.validate_due_date(due_date, now)

    def test_due_date_validation_rejects_non_datetime(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be a datetime"):
            Task.validate_due_date("tomorrow")  # type: ignore[arg-type]

    def test_due_date_validation_rejects_incompatible_time_zones(self) -> None:
        now = datetime(2030, 1, 1, tzinfo=timezone.utc)
        with self.assertRaisesRegex(ValueError, "compatible time zones"):
            Task.validate_due_date(datetime(2030, 1, 2), now)


class TaskTransitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Task("Transition test")

    def test_todo_can_transition_to_in_progress(self) -> None:
        self.assertTrue(self.task.can_transition(TaskStatus.IN_PROGRESS))

    def test_in_progress_can_transition_to_done(self) -> None:
        self.task.status = TaskStatus.IN_PROGRESS

        self.assertTrue(self.task.can_transition(TaskStatus.DONE))

    def test_done_cannot_transition_backwards(self) -> None:
        self.task.status = TaskStatus.DONE

        self.assertFalse(self.task.can_transition(TaskStatus.IN_PROGRESS))

    def test_any_active_status_can_transition_to_archived(self) -> None:
        for status in (TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE):
            with self.subTest(status=status):
                self.task.status = status
                self.assertTrue(self.task.can_transition(TaskStatus.ARCHIVED))

    def test_archived_is_a_terminal_status(self) -> None:
        self.task.status = TaskStatus.ARCHIVED

        for status in TaskStatus:
            with self.subTest(status=status):
                self.assertFalse(self.task.can_transition(status))

    def test_invalid_status_does_not_allow_transition(self) -> None:
        self.assertFalse(self.task.can_transition("DONE"))  # type: ignore[arg-type]


class TaskOverdueTests(unittest.TestCase):
    def test_task_is_overdue_when_past_due_and_active(self) -> None:
        now = datetime(2030, 1, 2)
        task = Task("Overdue task")
        task.due_date = now - timedelta(seconds=1)

        self.assertTrue(task.is_overdue(now))

    def test_task_is_not_overdue_when_due_at_current_time(self) -> None:
        now = datetime(2030, 1, 2)
        task = Task("Due now")
        task.due_date = now

        self.assertFalse(task.is_overdue(now))

    def test_task_is_not_overdue_when_due_in_future(self) -> None:
        now = datetime(2030, 1, 2)
        task = Task("Future task")
        task.due_date = now + timedelta(seconds=1)

        self.assertFalse(task.is_overdue(now))

    def test_task_without_due_date_is_not_overdue(self) -> None:
        self.assertFalse(Task("No deadline").is_overdue())

    def test_done_and_archived_tasks_are_not_overdue(self) -> None:
        now = datetime(2030, 1, 2)
        task = Task("Closed task")
        task.due_date = now - timedelta(days=1)

        for status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            with self.subTest(status=status):
                task.status = status
                self.assertFalse(task.is_overdue(now))

    def test_overdue_detection_rejects_incompatible_time_zones(self) -> None:
        task = Task(
            "Aware deadline", due_date=datetime.now(timezone.utc) + timedelta(days=1)
        )

        with self.assertRaisesRegex(ValueError, "compatible time zones"):
            task.is_overdue(datetime.now())


class TaskPriorityTests(unittest.TestCase):
    def test_higher_priority_compares_as_greater(self) -> None:
        urgent = Task("Urgent task", priority=TaskPriority.URGENT)
        high = Task("High task", priority=TaskPriority.HIGH)

        self.assertEqual(urgent.compare_priority(high), 1)

    def test_lower_priority_compares_as_less(self) -> None:
        low = Task("Low task", priority=TaskPriority.LOW)
        medium = Task("Medium task", priority=TaskPriority.MEDIUM)

        self.assertEqual(low.compare_priority(medium), -1)

    def test_equal_priorities_compare_as_equal(self) -> None:
        first = Task("First task", priority=TaskPriority.HIGH)
        second = Task("Second task", priority=TaskPriority.HIGH)

        self.assertEqual(first.compare_priority(second), 0)

    def test_priority_comparison_requires_another_task(self) -> None:
        task = Task("Valid task")

        with self.assertRaisesRegex(TypeError, "another Task"):
            task.compare_priority(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
