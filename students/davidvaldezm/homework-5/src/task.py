"""TaskFlow domain model and its business invariants."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from itertools import count


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


_task_ids = count(1)


@dataclass
class Task:  # pylint: disable=too-many-instance-attributes
    """A task whose state can only move forward through its lifecycle."""

    title: str
    description: str = ""
    priority: TaskPriority = TaskPriority.LOW
    due_date: datetime | None = None
    id: int = field(default_factory=lambda: next(_task_ids))
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)
    created_at: datetime = field(default_factory=datetime.now, init=False)
    updated_at: datetime = field(default_factory=datetime.now, init=False)

    def __post_init__(self) -> None:
        self.validate_title(self.title)
        self.validate_description(self.description)
        if not isinstance(self.priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority")
        if self.due_date is not None:
            self.validate_due_date(self.due_date)

    @staticmethod
    def validate_title(title: str) -> None:
        if not isinstance(title, str) or not title.strip() or len(title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_description(description: str) -> None:
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        if len(description) > 500:
            raise ValueError("Description must not exceed 500 characters")

    @staticmethod
    def validate_due_date(due_date: datetime) -> None:
        if not isinstance(due_date, datetime):
            raise ValueError("Due date must be a datetime")
        if due_date <= datetime.now():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status: TaskStatus) -> bool:
        """Return whether the requested lifecycle state change is allowed."""
        if not isinstance(new_status, TaskStatus) or self.status is TaskStatus.ARCHIVED:
            return False
        if new_status is TaskStatus.ARCHIVED:
            return True
        transitions = {
            TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
            TaskStatus.IN_PROGRESS: {TaskStatus.DONE},
            TaskStatus.DONE: set(),
        }
        return new_status in transitions[self.status]

    def transition_to(self, new_status: TaskStatus) -> None:
        if not self.can_transition(new_status):
            raise ValueError(
                f"Invalid transition from {self.status.value} to {new_status}"
            )
        self.status = new_status
        self.touch()

    def update_details(
        self,
        *,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        due_date: datetime | None = None,
    ) -> None:
        """Update mutable fields; archived tasks deliberately reject all changes."""
        if self.status is TaskStatus.ARCHIVED:
            raise ValueError("Archived tasks cannot be modified")
        if title is not None:
            self.validate_title(title)
            self.title = title
        if description is not None:
            self.validate_description(description)
            self.description = description
        if priority is not None:
            if not isinstance(priority, TaskPriority):
                raise ValueError("Priority must be a TaskPriority")
            self.priority = priority
        if due_date is not None:
            self.validate_due_date(due_date)
            self.due_date = due_date
        self.touch()

    def is_overdue(self, now: datetime | None = None) -> bool:
        current_time = now or datetime.now()
        return (
            self.status not in {TaskStatus.DONE, TaskStatus.ARCHIVED}
            and self.due_date is not None
            and self.due_date < current_time
        )

    def compare_priority(self, other_task: "Task") -> int:
        if not isinstance(other_task, Task):
            raise ValueError("Can only compare priority with another Task")
        return (self.priority > other_task.priority) - (
            self.priority < other_task.priority
        )

    def touch(self) -> None:
        """Refresh the modification timestamp after a legitimate mutation."""
        self.updated_at = datetime.now()
