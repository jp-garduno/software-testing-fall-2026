"""Task model for TaskFlow: validation, status lifecycle, overdue detection and priority."""

from datetime import datetime
from enum import Enum

TITLE_MIN_LENGTH = 3
TITLE_MAX_LENGTH = 100
DESCRIPTION_MAX_LENGTH = 500


class TaskStatus(Enum):
    """Lifecycle states of a task."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    """Priority levels; a higher value is more urgent (URGENT > HIGH > MEDIUM > LOW)."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class TaskStateError(ValueError):
    """Raised when an operation is not allowed in the task's current status."""


# The only forward step out of each state. ARCHIVED is handled apart: every
# state may move to it and nothing may leave it.
_NEXT_STATUS = {
    TaskStatus.TODO: TaskStatus.IN_PROGRESS,
    TaskStatus.IN_PROGRESS: TaskStatus.DONE,
}


def current_time():
    """Return the current time. Every time read goes through here so tests can replace the clock."""
    return datetime.now()


class Task:  # pylint: disable=too-many-instance-attributes
    """A unit of work: the seven fields of the specification plus the id the repository assigns."""

    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        self.validate_title(title)
        self.validate_description(description)
        self.validate_priority(priority)
        self.validate_due_date(due_date)
        self.id = None
        self.title = title.strip()
        self.description = description or ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = current_time()
        self.updated_at = self.created_at

    @staticmethod
    def validate_title(title):
        """Require a string of 3 to 100 characters, ignoring surrounding whitespace."""
        if not isinstance(title, str) or len(title.strip()) < TITLE_MIN_LENGTH:
            raise ValueError(f"Title must be at least {TITLE_MIN_LENGTH} characters")
        if len(title.strip()) > TITLE_MAX_LENGTH:
            raise ValueError(f"Title must not exceed {TITLE_MAX_LENGTH} characters")

    @staticmethod
    def validate_description(description):
        """Allow an empty description; reject one longer than 500 characters."""
        if description and len(description) > DESCRIPTION_MAX_LENGTH:
            raise ValueError(f"Description must not exceed {DESCRIPTION_MAX_LENGTH} characters")

    @staticmethod
    def validate_priority(priority):
        """Accept only TaskPriority members, so priorities stay comparable."""
        if not isinstance(priority, TaskPriority):
            raise ValueError(f"Priority must be a TaskPriority, got {priority!r}")

    @staticmethod
    def validate_due_date(due_date):
        """A due date is optional, but when present it must be in the future."""
        if due_date is not None and due_date <= current_time():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        """Return True if moving to new_status follows the allowed lifecycle."""
        if self.status is TaskStatus.ARCHIVED:
            return False
        if new_status is TaskStatus.ARCHIVED:
            return True
        return _NEXT_STATUS.get(self.status) is new_status

    def transition_to(self, new_status):
        """Move to new_status and return the previous status, or raise TaskStateError."""
        if not self.can_transition(new_status):
            target = getattr(new_status, "value", new_status)
            raise TaskStateError(f"Invalid transition from {self.status.value} to {target}")
        previous = self.status
        self.status = new_status
        self.touch()
        return previous

    def update(self, title=None, description=None, priority=None, due_date=None):
        """Change the given fields after validating all of them; archived tasks are read-only."""
        if self.status is TaskStatus.ARCHIVED:
            raise TaskStateError("Archived tasks cannot be modified")
        requested = {"title": title, "description": description, "priority": priority, "due_date": due_date}
        changes = {field: value for field, value in requested.items() if value is not None}
        if not changes:
            raise ValueError("No fields to update")
        for field, value in changes.items():
            _VALIDATORS[field](value)
        if "title" in changes:
            changes["title"] = changes["title"].strip()
        for field, value in changes.items():
            setattr(self, field, value)
        self.touch()

    def touch(self):
        """Record that the task was modified now."""
        self.updated_at = current_time()

    def is_overdue(self):
        """Overdue means past its due date while still open (neither DONE nor ARCHIVED)."""
        if self.due_date is None or self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        return current_time() > self.due_date

    def compare_priority(self, other):
        """Return 1 if this task is more urgent than other, -1 if less urgent, 0 if equal."""
        if self.priority.value > other.priority.value:
            return 1
        if self.priority.value < other.priority.value:
            return -1
        return 0


_VALIDATORS = {
    "title": Task.validate_title,
    "description": Task.validate_description,
    "priority": Task.validate_priority,
    "due_date": Task.validate_due_date,
}
