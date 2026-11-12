"""Task domain model for TaskFlow."""

from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Lifecycle states of a task."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    """Priority levels; the value defines the sort order."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


MIN_TITLE_LENGTH = 3
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500

_TRANSITIONS = {
    TaskStatus.TODO: (TaskStatus.IN_PROGRESS,),
    TaskStatus.IN_PROGRESS: (TaskStatus.DONE,),
    TaskStatus.DONE: (),
}


class Task:
    """A unit of work with validation and status lifecycle."""

    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Init."""
        self.validate_title(title)
        if due_date is not None:
            self.validate_due_date(due_date)
        self.title = title
        self.description = description[:MAX_DESCRIPTION_LENGTH] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    @staticmethod
    def validate_title(title):
        """Raise ValueError unless the title is 3-100 characters."""
        if not title or len(title) < MIN_TITLE_LENGTH:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_due_date(due_date):
        """Raise ValueError if the due date is not in the future."""
        if due_date <= datetime.now():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        """Return True if moving to ``new_status`` is a valid transition."""
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        return new_status in _TRANSITIONS[self.status]

    def is_overdue(self):
        """A task is overdue when past due and neither DONE nor ARCHIVED."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        """Return 1 if higher, -1 if lower, 0 if equal priority."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0

    def touch(self):
        """Refresh ``updated_at``."""
        self.updated_at = datetime.now()
