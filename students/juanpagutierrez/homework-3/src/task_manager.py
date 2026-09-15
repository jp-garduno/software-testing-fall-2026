"""Core task management logic (in-memory model backed by JSON storage)."""

import datetime

from storage import load_tasks, save_tasks

PRIORITY_LEVELS = ["low", "medium", "high"]


class TaskManager:
    """Keeps track of tasks and persists them to disk on every change."""

    def __init__(self, tasks=None):
        self.tasks = tasks if tasks else load_tasks()
        self.next_id = len(self.tasks) + 1

    def add_task(self, title, priority="medium", due_date=None):
        """Create a new task and persist it."""
        if priority not in PRIORITY_LEVELS:
            priority = "medium"
        task = {
            "id": self.next_id,
            "title": title,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": str(datetime.datetime.now()),
        }
        self.tasks.append(task)
        self.next_id += 1
        save_tasks(self.tasks)
        return task

    def complete_task(self, task_id):
        """Mark a task as completed by id. Returns True if found."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                save_tasks(self.tasks)
                return True
        return False

    def remove_task(self, task_id):
        """Remove a task by id. Returns True if it existed."""
        found = any(task["id"] == task_id for task in self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        save_tasks(self.tasks)
        return found

    def list_tasks(self, show_completed=True, filter_priority=None):
        """Return tasks, optionally hiding completed ones or filtering by priority."""
        result = []
        for task in self.tasks:
            if not show_completed and task["completed"]:
                continue
            if filter_priority is not None and task["priority"] != filter_priority:
                continue
            result.append(task)
        return result

    def get_tasks_by_priority(self):
        """Return tasks sorted by priority (high first), then creation date."""
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.tasks, key=lambda t: (order[t["priority"]], t["created_at"]))
