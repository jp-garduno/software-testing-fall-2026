"""Task model module representing tasks in the TaskFlow system."""

from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Lifecycle status states for tasks."""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    """Priority levels for tasks, ordered by severity."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Task:
    """Represents a task with validation, state transitions, and priority management."""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: Optional[datetime] = None,
        task_id: Optional[int] = None,
    ):
        self.validate_title(title)
        if due_date is not None:
            self.validate_due_date(due_date)

        self.id = task_id
        self.title = title
        self.description = description[:500] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @staticmethod
    def validate_title(title: str) -> None:
        """Validate title constraints (3-100 characters)."""
        if not title or not isinstance(title, str) or len(title) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    def validate_due_date(self, due_date: datetime) -> None:
        """Validate that due date is in the future."""
        if not isinstance(due_date, datetime):
            raise TypeError("Due date must be a datetime instance")
        if due_date < datetime.now():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status: TaskStatus) -> bool:
        """Check if transition to new_status is valid according to business rules."""
        if self.status == TaskStatus.ARCHIVED:
            return False

        if new_status == TaskStatus.ARCHIVED:
            return True

        valid_transitions = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
            TaskStatus.DONE: [],
        }

        return new_status in valid_transitions.get(self.status, [])

    def transition_to(self, new_status: TaskStatus) -> bool:
        """Execute a state transition if valid, updating updated_at timestamp."""
        if not self.can_transition(new_status):
            raise ValueError(f"Invalid transition from {self.status.value} to {new_status.value}")

        self.status = new_status
        self.updated_at = datetime.now()
        return True

    def is_overdue(self) -> bool:
        """Check if task is past its due date and not completed or archived."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task: "Task") -> int:
        """Compare priority with another task. Returns 1 if higher, -1 if lower, 0 if equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        elif self.priority.value < other_task.priority.value:
            return -1
        return 0

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        due_date: Optional[datetime] = None,
    ) -> None:
        """Update task attributes if the task is not archived."""
        if self.status == TaskStatus.ARCHIVED:
            raise ValueError("Cannot update archived task")

        if title is not None:
            self.validate_title(title)
            self.title = title

        if description is not None:
            self.description = description[:500]

        if priority is not None:
            self.priority = priority

        if due_date is not None:
            self.validate_due_date(due_date)
            self.due_date = due_date

        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert task model to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.name,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
