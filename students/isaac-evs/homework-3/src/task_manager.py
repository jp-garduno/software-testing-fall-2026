"""Simple in-memory task manager with priorities and completion tracking."""

import datetime
import json


class Task:
    """A single to-do item with a title, priority, and completion state."""

    def __init__(self, title, priority="medium"):
        self.title = title
        self.priority = priority
        self.done = False
        self.created_at = datetime.datetime.now()

    def complete(self):
        """Mark this task as done."""
        self.done = True

    def __repr__(self):
        return f"Task({self.title}, done={self.done})"


class TaskManager:
    """Manages a collection of Task objects."""

    def __init__(self):
        self.tasks = []

    def add_task(self, title, priority="medium"):
        """Create a new task and add it to the manager."""
        task = Task(title, priority)
        self.tasks.append(task)
        return task

    def remove_task(self, title):
        """Remove a task by title. Returns True if a task was removed."""
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return True
        return False

    def get_pending_tasks(self):
        """Return all tasks that are not yet completed."""
        return [task for task in self.tasks if not task.done]

    def get_completed_tasks(self):
        """Return all tasks that have been completed."""
        return [task for task in self.tasks if task.done]

    def complete_task(self, title):
        """Mark a task as complete by title. Returns True if found."""
        for task in self.tasks:
            if task.title == title:
                task.complete()
                return True
        return False

    def to_json(self):
        """Serialize all tasks to a JSON string."""
        data = [
            {"title": task.title, "priority": task.priority, "done": task.done}
            for task in self.tasks
        ]
        return json.dumps(data)

    def count_by_priority(self, priority):
        """Count how many tasks match the given priority."""
        count = 0
        for task in self.tasks:
            if task.priority == priority:
                count = count + 1
        return count
