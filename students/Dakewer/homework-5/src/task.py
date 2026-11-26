"""Task domain model for TaskFlow.

Contains the enums, validation rules, status-transition logic, overdue
detection and priority comparison. This module has no external dependencies
so it can be unit tested in complete isolation.
"""

from datetime import datetime
from enum import Enum

MIN_TITLE_LENGTH = 3
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500


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


# Forward-only transitions. ARCHIVED is handled separately in can_transition.
_ALLOWED_TRANSITIONS = {
    TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
    TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
    TaskStatus.DONE: [],
}


class Task:
    """A single task with validation and lifecycle rules."""

    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        self.validate_title(title)
        if due_date:
            self.validate_due_date(due_date)

        self.id = None  # assigned by the repository when saved
        self.title = title
        self.description = self.normalize_description(description)
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    @staticmethod
    def validate_title(title):
        if not title or len(title) < MIN_TITLE_LENGTH:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_due_date(due_date):
        if due_date < datetime.now():
            raise ValueError("Due date must be in the future")

    @staticmethod
    def normalize_description(description):
        """Return the description truncated to the maximum allowed length."""
        if not description:
            return ""
        return description[:MAX_DESCRIPTION_LENGTH]

    def can_transition(self, new_status):
        """Return True if moving to ``new_status`` is a valid transition."""
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        return new_status in _ALLOWED_TRANSITIONS.get(self.status, [])

    def is_overdue(self):
        """A task is overdue when its due date has passed and it is still open."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        """Return 1 if higher priority than ``other_task``, -1 if lower, 0 if equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0

    def touch(self):
        """Refresh ``updated_at``."""
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"Task(id={self.id!r}, title={self.title!r}, status={self.status.value})"
