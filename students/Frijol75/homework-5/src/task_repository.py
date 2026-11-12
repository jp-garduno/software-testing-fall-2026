"""Data access layer for tasks (intended to be mocked in tests)."""

from typing import Any, List, Optional
from task import Task, TaskPriority, TaskStatus


class TaskRepository:
    """Interface / data access layer for task persistence."""

    def __init__(self, database: Optional[Any] = None):
        self.database = database

    def save(self, task: Task) -> Task:
        """Save or update task in the persistence store."""
        raise NotImplementedError("Must be mocked in tests")

    def find_by_id(self, task_id: Any) -> Optional[Task]:
        """Find task by unique identifier."""
        raise NotImplementedError("Must be mocked in tests")

    def find_by_title(self, title: str) -> Optional[Task]:
        """Find task by exact title match."""
        raise NotImplementedError("Must be mocked in tests")

    def find_all(self) -> List[Task]:
        """Retrieve all tasks."""
        raise NotImplementedError("Must be mocked in tests")

    def delete(self, task_id: Any) -> bool:
        """Permanently delete a task by ID."""
        raise NotImplementedError("Must be mocked in tests")

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        """Filter tasks by status."""
        raise NotImplementedError("Must be mocked in tests")

    def filter_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Filter tasks by priority."""
        raise NotImplementedError("Must be mocked in tests")

    def search_by_title(self, query: str) -> List[Task]:
        """Search tasks by title substring."""
        raise NotImplementedError("Must be mocked in tests")
