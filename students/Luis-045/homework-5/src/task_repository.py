"""Persistence contract; an adapter translates database failures to RepositoryError."""

from typing import Protocol

from .task import Task


class RepositoryError(RuntimeError):
    """The persistence operation could not be completed."""


class TaskRepository(Protocol):
    """Boundary for storage operations, replaced by test doubles in this project."""

    def save(self, task: Task) -> None:
        """Insert or replace a task using its id."""
        ...

    def find_by_id(self, task_id: str) -> Task | None:
        """Return the identified task, or None when it is absent."""
        ...

    def find_by_title(self, title: str) -> Task | None:
        """Find an exact, case-sensitive title across all stored tasks."""
        ...

    def find_all(self) -> list[Task]:
        """Return tasks for searching, filtering and overdue checks."""
        ...

    def delete(self, task_id: str) -> None:
        """Permanently remove data; TaskService uses soft deletion instead."""
        ...
