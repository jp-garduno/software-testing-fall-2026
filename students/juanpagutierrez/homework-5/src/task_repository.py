"""Data access layer for tasks.

TaskRepository talks to a key-value ``database`` client (``get``, ``put``,
``remove`` and ``values``). The client is the persistence boundary and is
replaced by a mock in tests.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from task import TaskPriority, TaskStatus


class RepositoryError(Exception):
    """Raised when the underlying database fails."""


@dataclass(frozen=True)
class TaskQuery:
    """Search criteria. Every field left as None matches any task.

    due_after and due_before are inclusive bounds on due_date; a task without a
    due date never matches a date range. title_contains is case-insensitive.
    """

    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_after: Optional[datetime] = None
    due_before: Optional[datetime] = None
    title_contains: Optional[str] = None

    def __post_init__(self):
        if self.due_after is not None and self.due_before is not None and self.due_after > self.due_before:
            raise ValueError("due_after must not be later than due_before")

    def matches(self, task):
        if self.status is not None and task.status != self.status:
            return False
        if self.priority is not None and task.priority != self.priority:
            return False
        if not self._matches_date_range(task.due_date):
            return False
        if self.title_contains is not None:
            return self.title_contains.lower() in task.title.lower()
        return True

    def _matches_date_range(self, due_date):
        if self.due_after is None and self.due_before is None:
            return True
        if due_date is None:
            return False
        if self.due_after is not None and due_date < self.due_after:
            return False
        return self.due_before is None or due_date <= self.due_before


class TaskRepository:

    def __init__(self, database):
        self.database = database

    def _call(self, operation, *args):
        try:
            return getattr(self.database, operation)(*args)
        except Exception as error:  # pylint: disable=broad-exception-caught
            # Any driver failure is translated so callers depend on one error type.
            raise RepositoryError(f"Database {operation} failed: {error}") from error

    def save(self, task):
        self._call("put", task.id, task)
        return task

    def find_by_id(self, task_id):
        return self._call("get", task_id)

    def find_by_title(self, title):
        return next((task for task in self.find_all() if task.title == title), None)

    def find_all(self):
        return list(self._call("values"))

    def delete(self, task_id):
        """Permanently remove a task. Returns False when it did not exist."""
        if self.find_by_id(task_id) is None:
            return False
        self._call("remove", task_id)
        return True

    def search(self, query):
        """Return the stored tasks matching every criterion of a TaskQuery."""
        return [task for task in self.find_all() if query.matches(task)]
