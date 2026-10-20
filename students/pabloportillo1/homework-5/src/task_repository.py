from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from task import Task, TaskPriority, TaskStatus


class DatabaseError(Exception):
    """Raised by a database driver when a storage operation fails."""


class RepositoryError(RuntimeError):
    """Raised when the repository cannot complete an operation because the database failed."""


class Database(Protocol):
    """Storage contract the repository relies on; a production driver or a test double implements it."""

    def insert(self, task: Task) -> int:
        """Store a new task and return the identifier the database assigned to it."""

    def update(self, task_id: int, task: Task) -> None:
        """Replace the stored task that has the given identifier."""

    def get(self, task_id: int) -> Task | None:
        """Return the stored task, or None when the identifier is unknown."""

    def delete(self, task_id: int) -> bool:
        """Remove the stored task and return True, or return False when the identifier is unknown."""

    def all(self) -> list[Task]:
        """Return every stored task."""


@dataclass(frozen=True)
class TaskFilter:
    """Search criteria; every criterion left as None matches all tasks, and the rest must all hold."""

    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_from: datetime | None = None
    due_to: datetime | None = None
    title_contains: str | None = None

    def __post_init__(self):
        if self.due_from is not None and self.due_to is not None and self.due_from > self.due_to:
            raise ValueError("due_from must not be later than due_to")

    def matches(self, task):
        """Return True when the task satisfies every criterion that is set."""
        if self.status is not None and task.status is not self.status:
            return False
        if self.priority is not None and task.priority is not self.priority:
            return False
        if self.title_contains and self.title_contains.strip().casefold() not in task.title.casefold():
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
    """Data access layer: persists tasks through a Database and turns its failures into RepositoryError."""

    def __init__(self, database: Database):
        self._database = database

    def save(self, task):
        """Insert a new task (assigning its task_id) or update an existing one, and return it."""
        failure = f"Could not save task '{task.title}'"
        if task.task_id is None:
            task.task_id = self._run(failure, self._database.insert, task)
        else:
            self._run(failure, self._database.update, task.task_id, task)
        return task

    def find_by_id(self, task_id):
        """Return the task with the given identifier, or None."""
        return self._run(f"Could not load task {task_id}", self._database.get, task_id)

    def find_by_title(self, title):
        """Return the task whose title matches, ignoring case and surrounding whitespace, or None."""
        wanted = title.strip().casefold()
        return next((task for task in self.find_all() if task.title.casefold() == wanted), None)

    def find_all(self):
        """Return every stored task."""
        return self._run("Could not load tasks", self._database.all)

    def delete(self, task_id):
        """Permanently remove a task; return False when it did not exist."""
        return self._run(f"Could not delete task {task_id}", self._database.delete, task_id)

    def search(self, task_filter):
        """Return the tasks matching task_filter, ordered URGENT > HIGH > MEDIUM > LOW."""
        matches = [task for task in self.find_all() if task_filter.matches(task)]
        return sorted(matches, key=lambda task: task.priority.value, reverse=True)

    @staticmethod
    def _run(failure, operation, *args):
        try:
            return operation(*args)
        except DatabaseError as error:
            raise RepositoryError(failure) from error
