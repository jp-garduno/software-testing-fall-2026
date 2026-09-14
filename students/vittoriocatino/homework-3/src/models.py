"""Domain entities for the in-memory task tracker."""

from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(str, Enum):
    """States that a task can have during its lifetime."""

    OPEN = "open"
    COMPLETED = "completed"


@dataclass
class Task:
    """A small work item with a priority, labels, and completion state."""

    identifier: int
    title: str
    priority: int
    tags: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.OPEN

    @property
    def is_completed(self) -> bool:
        """Return whether the task has been marked as completed."""

        return self.status is TaskStatus.COMPLETED

    def mark_complete(self) -> None:
        """Mark this task as completed."""

        self.status = TaskStatus.COMPLETED

    def reopen(self) -> None:
        """Return this task to the open state."""

        self.status = TaskStatus.OPEN

    def to_dict(self) -> dict[str, object]:
        """Return a serializable representation of the task."""

        return {
            "id": self.identifier,
            "title": self.title,
            "priority": self.priority,
            "tags": list(self.tags),
            "status": self.status.value,
        }
