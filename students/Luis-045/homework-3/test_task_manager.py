import unittest

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
        manager.add_task("Homework", "Finish static testing homework", "high")
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

    def test_summary(self):
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.complete_task("Task 1")
        self.assertEqual(
            manager.summary(),
            "Task summary -> total tasks: 2, completed tasks: 1, pending tasks: 1, completion tracking enabled",
        )


if __name__ == "__main__":
    unittest.main()