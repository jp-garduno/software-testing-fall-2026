"""Data access layer for TaskFlow.

TaskRepository adds the task-specific logic (lookups, search and filtering, error
translation) on top of a low-level ``database`` object. The database is the external
dependency: it is mocked in the tests and only needs four methods::

    database.upsert(key, value)   -> None
    database.get(key)             -> value | None
    database.values()             -> iterable of values
    database.remove(key)          -> bool (True if something was removed)
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from task import Task, TaskPriority, TaskStatus


class RepositoryError(Exception):
    """Raised when the underlying database fails. Wraps the original exception."""


class TaskRepository:
    """CRUD, search and filter operations for tasks."""

    def __init__(self, database) -> None:
        self.database = database

    # ------------------------------------------------------------------ #
    # CRUD
    # ------------------------------------------------------------------ #
    def save(self, task: Task) -> Task:
        """Insert or update a task."""
        try:
            self.database.upsert(task.id, task)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise RepositoryError(f"Could not save task {task.id}: {exc}") from exc
        return task

    def find_by_id(self, task_id: str) -> Task | None:
        """Return the task with that id, or None."""
        try:
            return self.database.get(task_id)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise RepositoryError(f"Could not read task {task_id}: {exc}") from exc

    def find_all(self) -> list[Task]:
        """Return every stored task."""
        try:
            return list(self.database.values())
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise RepositoryError(f"Could not list tasks: {exc}") from exc

    def find_by_title(self, title: str) -> Task | None:
        """Exact, case-insensitive title lookup (used to enforce unique titles)."""
        wanted = title.strip().casefold()
        for task in self.find_all():
            if task.title.strip().casefold() == wanted:
                return task
        return None

    def delete(self, task_id: str) -> bool:
        """Permanently remove a task. Returns False when it did not exist."""
        try:
            return bool(self.database.remove(task_id))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise RepositoryError(f"Could not delete task {task_id}: {exc}") from exc

    # ------------------------------------------------------------------ #
    # Search and filter
    # ------------------------------------------------------------------ #
    def search(  # pylint: disable=too-many-arguments
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        due_after: datetime | None = None,
        due_before: datetime | None = None,
        title_contains: str | None = None,
    ) -> list[Task]:
        """Return the tasks matching every given filter, highest priority first.

        Filters left as None are ignored, so ``search()`` returns everything.
        The date range is inclusive; tasks without a due date never match a range.
        """
        if due_after and due_before and due_after > due_before:
            raise ValueError("due_after must not be later than due_before")

        predicates: list[Callable[[Task], bool]] = []
        if status is not None:
            predicates.append(lambda task: task.status == status)
        if priority is not None:
            predicates.append(lambda task: task.priority == priority)
        if due_after is not None:
            predicates.append(lambda task: task.due_date is not None and task.due_date >= due_after)
        if due_before is not None:
            predicates.append(lambda task: task.due_date is not None and task.due_date <= due_before)
        if title_contains and title_contains.strip():
            needle = title_contains.strip().casefold()
            predicates.append(lambda task: needle in task.title.casefold())

        results = [task for task in self.find_all() if all(check(task) for check in predicates)]
        return sorted(results, key=lambda task: task.priority.value, reverse=True)
