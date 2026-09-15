# pylint: disable=too-many-public-methods
import unittest
from contextlib import redirect_stdout
from io import StringIO

from src.app import create_demo_manager, main, print_summary, print_tasks
from src.task import Task
from src.task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def test_task_defaults(self):
        task = Task("Study")
        self.assertEqual(task.title, "Study")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)

    def test_mark_completed(self):
        task = Task("Study")
        task.mark_completed()
        self.assertTrue(task.completed)

    def test_update_priority(self):
        task = Task("Study")
        task.update_priority("high")
        self.assertEqual(task.priority, "high")

    def test_invalid_priority(self):
        task = Task("Study")
        with self.assertRaises(ValueError):
            task.update_priority("urgent")

    def test_add_and_find_task(self):
        manager = TaskManager()
        manager.add_task(
            "Homework",
            "Finish static testing homework",
            "high",
        )
        task = manager.find_task("Homework")

        self.assertIsNotNone(task)
        self.assertEqual(task.priority, "high")

    def test_complete_task(self):
        manager = TaskManager()
        manager.add_task("Homework")

        self.assertTrue(manager.complete_task("Homework"))
        self.assertTrue(manager.find_task("Homework").completed)

    def test_remove_task(self):
        manager = TaskManager()
        manager.add_task("Homework")

        self.assertTrue(manager.remove_task("Homework"))
        self.assertEqual(manager.count_tasks(), 0)

    def test_tasks_by_priority(self):
        manager = TaskManager()
        manager.add_task("Task 1", priority="high")
        manager.add_task("Task 2", priority="low")
        manager.add_task("Task 3", priority="high")

        high_priority = manager.tasks_by_priority("high")

        self.assertEqual(len(high_priority), 2)

    def test_completion_percentage(self):
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.complete_task("Task 1")

        self.assertEqual(manager.completion_percentage(), 50.0)

    def test_task_to_dict(self):
        task = Task("Study", "Review notes", "high")

        expected = {
            "title": "Study",
            "description": "Review notes",
            "priority": "high",
            "completed": False,
        }

        self.assertEqual(task.to_dict(), expected)

    def test_task_string(self):
        task = Task("Study", priority="high")

        self.assertEqual(str(task), "Study | high | Pending")

        task.mark_completed()

        self.assertEqual(str(task), "Study | high | Done")

    def test_change_priority(self):
        manager = TaskManager()
        manager.add_task("Homework")

        result = manager.change_priority("Homework", "high")

        self.assertTrue(result)
        self.assertEqual(manager.find_task("Homework").priority, "high")

    def test_change_priority_missing_task(self):
        manager = TaskManager()

        self.assertFalse(manager.change_priority("Missing", "high"))

    def test_complete_missing_task(self):
        manager = TaskManager()

        self.assertFalse(manager.complete_task("Missing"))

    def test_remove_missing_task(self):
        manager = TaskManager()

        self.assertFalse(manager.remove_task("Missing"))

    def test_pending_and_completed_tasks(self):
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.complete_task("Task 1")

        self.assertEqual(len(manager.pending_tasks()), 1)
        self.assertEqual(len(manager.completed_tasks()), 1)

    def test_clear_completed(self):
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.complete_task("Task 1")

        manager.clear_completed()

        self.assertEqual(manager.count_tasks(), 1)
        self.assertEqual(manager.find_task("Task 2").title, "Task 2")

    def test_completion_percentage_empty(self):
        manager = TaskManager()

        self.assertEqual(manager.completion_percentage(), 0.0)

    def test_create_demo_manager(self):
        manager = create_demo_manager()

        self.assertEqual(manager.count_tasks(), 3)
        self.assertTrue(manager.find_task("Study").completed)

    def test_print_tasks(self):
        manager = TaskManager()
        manager.add_task("Homework")

        output = StringIO()

        with redirect_stdout(output):
            print_tasks(manager)

        self.assertIn("Homework", output.getvalue())

    def test_print_summary(self):
        manager = TaskManager()
        manager.add_task("Homework")

        output = StringIO()

        with redirect_stdout(output):
            print_summary(manager)

        self.assertIn("Task summary", output.getvalue())

    def test_main(self):
        output = StringIO()

        with redirect_stdout(output):
            main()

        result = output.getvalue()

        self.assertIn("TODO LIST", result)
        self.assertIn("Study", result)
        self.assertIn("Task summary", result)

    def test_summary(self):
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.complete_task("Task 1")

        expected = (
            "Task summary -> total tasks: 2, "
            "completed tasks: 1, "
            "pending tasks: 1, "
            "completion tracking enabled"
        )

        self.assertEqual(manager.summary(), expected)


if __name__ == "__main__":
    unittest.main()
