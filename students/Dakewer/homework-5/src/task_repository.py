"""Data access layer for tasks.

The repository talks to a ``database`` object that behaves like a mutable
mapping (``db[key] = value``, ``db.get(key)``, ``del db[key]``, ``db.values()``).
Tests replace both the repository (with mocks/fakes) and the database (with
failing doubles) so no real persistence is ever touched.
"""

import logging

from task import Task

logger = logging.getLogger(__name__)


class RepositoryError(Exception):
    """Raised when the underlying database fails."""


class TaskRepository:
    """CRUD, search and filter operations for tasks."""

    def __init__(self, database):
        self.database = database
        self._next_id = 1

    def save(self, task):
        """Insert or update a task, assigning an id on first save."""
        try:
            if task.id is None:
                task.id = self._next_id
                self._next_id += 1
            self.database[task.id] = task
        except Exception as exc:
            logger.error("Failed to save task: %s", exc)
            raise RepositoryError("Could not save task") from exc
        return task

    def find_by_id(self, task_id):
        """Return the task with ``task_id`` or None."""
        return self._read(lambda: self.database.get(task_id))

    def find_by_title(self, title):
        """Return the task whose title matches exactly, or None."""
        for task in self.find_all():
            if task.title == title:
                return task
        return None

    def find_all(self):
        """Return every stored task."""
        return self._read(lambda: list(self.database.values()))

    def delete(self, task_id):
        """Permanently remove a task. Returns True if something was removed."""
        try:
            if task_id not in self.database:
                return False
            del self.database[task_id]
        except Exception as exc:
            logger.error("Failed to delete task %s: %s", task_id, exc)
            raise RepositoryError("Could not delete task") from exc
        return True

    def search(self, status=None, priority=None, due_from=None, due_to=None, title_contains=None):
        """Return tasks matching every provided filter (filters are ANDed)."""
        results = self.find_all()

        if status is not None:
            results = [t for t in results if t.status == status]
        if priority is not None:
            results = [t for t in results if t.priority == priority]
        if due_from is not None:
            results = [t for t in results if t.due_date and t.due_date >= due_from]
        if due_to is not None:
            results = [t for t in results if t.due_date and t.due_date <= due_to]
        if title_contains:
            needle = title_contains.lower()
            results = [t for t in results if needle in t.title.lower()]

        return results

    @staticmethod
    def _read(operation):
        try:
            return operation()
        except Exception as exc:
            logger.error("Failed to read tasks: %s", exc)
            raise RepositoryError("Could not read tasks") from exc


__all__ = ["Task", "TaskRepository", "RepositoryError"]
