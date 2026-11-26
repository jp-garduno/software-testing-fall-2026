"""Data layer for TaskFlow: CRUD, search and filtering on top of an injected database client."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from task import TaskPriority, TaskStatus

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Raised by a database client when the storage operation itself fails."""


class RepositoryError(Exception):
    """Raised by the repository when the database could not complete an operation."""


class Database(ABC):
    """Contract of the storage client. Production plugs in a real adapter; tests use mocks or a fake."""

    @abstractmethod
    def insert(self, record):
        """Store a new record and return the id generated for it."""

    @abstractmethod
    def update(self, record_id, record):
        """Replace the record stored under record_id."""

    @abstractmethod
    def get(self, record_id):
        """Return the record stored under record_id, or None."""

    @abstractmethod
    def get_all(self):
        """Return every stored record."""

    @abstractmethod
    def remove(self, record_id):
        """Delete the record under record_id; return True if something was deleted."""


@dataclass(frozen=True)
class TaskFilter:
    """Search criteria. Criteria left as None are ignored; the rest must all match (AND)."""

    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_from: datetime | None = None
    due_to: datetime | None = None
    title_contains: str | None = None

    def __post_init__(self):
        if self.due_from is not None and self.due_to is not None and self.due_from > self.due_to:
            raise ValueError("due_from must not be later than due_to")

    def matches(self, task):
        """Return True if the task satisfies every criterion that was given."""
        if self.status is not None and task.status is not self.status:
            return False
        if self.priority is not None and task.priority is not self.priority:
            return False
        if self.title_contains and self.title_contains.casefold() not in task.title.casefold():
            return False
        return self._due_date_in_range(task.due_date)

    def _due_date_in_range(self, due_date):
        if self.due_from is None and self.due_to is None:
            return True
        if due_date is None:
            return False
        if self.due_from is not None and due_date < self.due_from:
            return False
        return self.due_to is None or due_date <= self.due_to


class TaskRepository:
    """Persists tasks through a Database client and turns storage failures into RepositoryError."""

    def __init__(self, database):
        self.database = database

    def save(self, task):
        """Insert a new task, assigning its id, or update one that already has an id."""
        if task.id is None:
            task.id = self._run("insert", task)
        else:
            self._run("update", task.id, task)
        return task

    def find_by_id(self, task_id):
        """Return the task with that id, or None."""
        return self._run("get", task_id)

    def find_all(self):
        """Return every stored task."""
        return list(self._run("get_all"))

    def find_by_title(self, title):
        """Return the task whose title matches exactly, ignoring case and surrounding spaces."""
        wanted = title.strip().casefold()
        return next((task for task in self.find_all() if task.title.casefold() == wanted), None)

    def search(self, task_filter):
        """Return the tasks that match a TaskFilter."""
        return [task for task in self.find_all() if task_filter.matches(task)]

    def delete(self, task_id):
        """Permanently delete a task; return False if there was nothing to delete."""
        return bool(self._run("remove", task_id))

    def _run(self, operation, *args):
        try:
            return getattr(self.database, operation)(*args)
        except DatabaseError as error:
            logger.error("Database operation '%s' failed: %s", operation, error)
            raise RepositoryError(f"Database operation '{operation}' failed") from error
