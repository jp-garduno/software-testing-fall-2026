"""In-memory task repository used behind the service boundary."""

from datetime import datetime

from src.task import Task, TaskPriority, TaskStatus


class RepositoryError(Exception):
    """Base error for repository operations."""


class DuplicateTaskError(ValueError):
    """Raised when a task title or identifier is already in use."""


class TaskRepository:
    """Store tasks in memory while exposing CRUD and filtering operations."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def save(self, task: Task) -> Task:
        if not isinstance(task, Task):
            raise TypeError("Only Task instances can be saved")

        for task_id, existing in self._tasks.items():
            if existing.title == task.title and task_id != task.id:
                raise DuplicateTaskError(
                    f"Task with title '{task.title}' already exists"
                )

        if task.id is None:
            task.id = self._next_id
            self._next_id += 1
        elif task.id in self._tasks and self._tasks[task.id] is not task:
            raise DuplicateTaskError(f"Task ID {task.id} is already in use")

        self._tasks[task.id] = task
        return task

    def find_by_id(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def find_by_title(self, title: str) -> Task | None:
        return next(
            (task for task in self._tasks.values() if task.title == title), None
        )

    def find_all(self) -> list[Task]:
        return [self._tasks[task_id] for task_id in sorted(self._tasks)]

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def search(  # pylint: disable=too-many-arguments
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        due_after: datetime | None = None,
        due_before: datetime | None = None,
        title: str | None = None,
    ) -> list[Task]:
        if status is not None and not isinstance(status, TaskStatus):
            raise ValueError("Status must be a TaskStatus value")
        if priority is not None and not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority value")
        if due_after is not None and not isinstance(due_after, datetime):
            raise ValueError("due_after must be a datetime")
        if due_before is not None and not isinstance(due_before, datetime):
            raise ValueError("due_before must be a datetime")
        if due_after is not None and due_before is not None and due_after > due_before:
            raise ValueError("due_after must not be later than due_before")
        if title is not None and not isinstance(title, str):
            raise ValueError("Title search must be a string")

        query = title.casefold() if title is not None else None
        return [
            task
            for task in self.find_all()
            if (status is None or task.status == status)
            and (priority is None or task.priority == priority)
            and (
                due_after is None
                or (task.due_date is not None and task.due_date >= due_after)
            )
            and (
                due_before is None
                or (task.due_date is not None and task.due_date <= due_before)
            )
            and (query is None or query in task.title.casefold())
        ]
