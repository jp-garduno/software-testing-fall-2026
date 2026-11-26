"""Task model with validation, status transitions, overdue detection, and priority comparison."""

from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task status states."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    """Task priority levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Task:
    """Domain model representing a task."""

    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        self.validate_title(title)
        if due_date is not None:
            self.validate_due_date(due_date)

        self.title = title
        self.description = description[:500] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @staticmethod
    def validate_title(title):
        """Validate title length between 3 and 100 characters."""
        if not title or len(title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_due_date(due_date):
        """Validate that due_date is in the future."""
        if due_date < datetime.now():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        """Check if transition to new_status is valid."""
        if self.status == TaskStatus.ARCHIVED:
            return False

        if new_status == TaskStatus.ARCHIVED:
            return True

        transitions = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
            TaskStatus.DONE: [],
        }

        return new_status in transitions.get(self.status, [])

    def is_overdue(self):
        """Check if task is overdue."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        """Compare priority with another task: 1 if higher, -1 if lower, 0 if equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0
