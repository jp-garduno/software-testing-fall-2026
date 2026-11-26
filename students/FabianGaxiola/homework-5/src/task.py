"""Task model and its business-level validation rules."""

from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Task:  # pylint: disable=too-many-instance-attributes
    """A task with validated attributes and lifecycle helpers."""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: datetime | None = None,
    ) -> None:
        self.validate_title(title)
        self.validate_description(description)
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority value")
        if due_date is not None:
            self.validate_due_date(due_date)

        now = datetime.now(due_date.tzinfo if due_date else None)
        self.id: int | None = None
        self.title = title
        self.description = description
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = now
        self.updated_at = now

    @staticmethod
    def validate_title(title: str) -> None:
        if not isinstance(title, str) or len(title) < 3:
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
    def validate_due_date(due_date: datetime, now: datetime | None = None) -> None:
        if not isinstance(due_date, datetime):
            raise ValueError("Due date must be a datetime")
        current_time = now or datetime.now(due_date.tzinfo)
        if current_time.tzinfo is None and due_date.tzinfo is not None:
            raise ValueError("Due date and current time must use compatible time zones")
        if current_time.tzinfo is not None and due_date.tzinfo is None:
            raise ValueError("Due date and current time must use compatible time zones")
        if due_date <= current_time:
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status: TaskStatus) -> bool:
        if not isinstance(new_status, TaskStatus):
            return False
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True

        transitions = {
            TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
            TaskStatus.IN_PROGRESS: {TaskStatus.DONE},
            TaskStatus.DONE: set(),
        }
        return new_status in transitions.get(self.status, set())

    def is_overdue(self, now: datetime | None = None) -> bool:
        if self.status in {TaskStatus.DONE, TaskStatus.ARCHIVED}:
            return False
        if self.due_date is None:
            return False

        current_time = now or datetime.now(self.due_date.tzinfo)
        if current_time.tzinfo is None and self.due_date.tzinfo is not None:
            raise ValueError("Due date and current time must use compatible time zones")
        if current_time.tzinfo is not None and self.due_date.tzinfo is None:
            raise ValueError("Due date and current time must use compatible time zones")
        return self.due_date < current_time

    def compare_priority(self, other_task: "Task") -> int:
        if not isinstance(other_task, Task):
            raise TypeError("Priority can only be compared with another Task")
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0
