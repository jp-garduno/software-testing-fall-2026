"""Task model: data, validation, status transitions, overdue detection and priority."""

import uuid
from datetime import datetime
from enum import Enum

from errors import ArchivedTaskError, InvalidTransitionError, TaskValidationError

TITLE_MIN_LENGTH = 3
TITLE_MAX_LENGTH = 100
DESCRIPTION_MAX_LENGTH = 500


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    """Priority levels; a higher value means a more important task."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


# Forward-only paths. ARCHIVED is reachable from every non-archived state and is terminal.
_FORWARD_TRANSITIONS = {
    TaskStatus.TODO: TaskStatus.IN_PROGRESS,
    TaskStatus.IN_PROGRESS: TaskStatus.DONE,
}


class Task:  # pylint: disable=too-many-instance-attributes
    """A unit of work tracked by TaskFlow.

    ``now`` can be injected so that tests control the clock instead of depending
    on the real time.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        title,
        description="",
        priority=TaskPriority.LOW,
        due_date=None,
        now=None,
    ):
        now = now or datetime.now()
        self.validate_title(title)
        self.validate_description(description)
        self.validate_priority(priority)
        if due_date is not None:
            self.validate_due_date(due_date, now)

        self.task_id = uuid.uuid4().hex
        self.title = title.strip()
        self.description = description or ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = now
        self.updated_at = now

    # ------------------------------------------------------------------ validation
    @staticmethod
    def validate_title(title):
        if not isinstance(title, str) or len(title.strip()) < TITLE_MIN_LENGTH:
            raise TaskValidationError(f"Title must be at least {TITLE_MIN_LENGTH} characters")
        if len(title.strip()) > TITLE_MAX_LENGTH:
            raise TaskValidationError(f"Title must not exceed {TITLE_MAX_LENGTH} characters")

    @staticmethod
    def validate_description(description):
        if description and len(description) > DESCRIPTION_MAX_LENGTH:
            raise TaskValidationError(f"Description must not exceed {DESCRIPTION_MAX_LENGTH} characters")

    @staticmethod
    def validate_priority(priority):
        if not isinstance(priority, TaskPriority):
            raise TaskValidationError(f"Invalid priority: {priority!r}")

    @staticmethod
    def validate_due_date(due_date, now=None):
        if not isinstance(due_date, datetime):
            raise TaskValidationError("Due date must be a datetime")
        if due_date <= (now or datetime.now()):
            raise TaskValidationError("Due date must be in the future")

    # ----------------------------------------------------------------- transitions
    def can_transition(self, new_status):
        """Return True when moving from the current status to ``new_status`` is allowed."""
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        return _FORWARD_TRANSITIONS.get(self.status) == new_status

    def transition_to(self, new_status, now=None):
        """Change the status, enforcing the transition rules. Returns the previous status."""
        if not self.can_transition(new_status):
            raise InvalidTransitionError(f"Invalid transition from {self.status.value} to {new_status.value}")
        old_status = self.status
        self.status = new_status
        self.touch(now)
        return old_status

    # --------------------------------------------------------------------- updates
    def update(self, now=None, **changes):
        """Update title, description, priority and/or due_date after validating them all.

        Nothing changes if any value is invalid. Archived tasks cannot be modified.
        """
        if self.status == TaskStatus.ARCHIVED:
            raise ArchivedTaskError("Archived tasks cannot be modified")
        allowed = {"title", "description", "priority", "due_date"}
        unknown = set(changes) - allowed
        if unknown:
            raise TaskValidationError(f"Cannot update field(s): {', '.join(sorted(unknown))}")

        now = now or datetime.now()
        validators = {
            "title": self.validate_title,
            "description": self.validate_description,
            "priority": self.validate_priority,
            "due_date": lambda value: self.validate_due_date(value, now),
        }
        for field, value in changes.items():
            validators[field](value)
        for field, value in changes.items():
            setattr(self, field, value.strip() if field == "title" else value)
        self.touch(now)

    def touch(self, now=None):
        self.updated_at = now or datetime.now()

    # --------------------------------------------------------------------- queries
    def is_overdue(self, now=None):
        """Overdue = has a due date in the past and is neither DONE nor ARCHIVED."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED) or self.due_date is None:
            return False
        return (now or datetime.now()) > self.due_date

    def compare_priority(self, other_task):
        """Return 1 if this task is more important than ``other_task``, -1 if less, 0 if equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0

    def sort_key(self):
        """Key for sorting URGENT > HIGH > MEDIUM > LOW, then earliest due date, then title."""
        due = self.due_date or datetime.max
        return (-self.priority.value, due, self.title.lower())

    def __repr__(self):
        return f"Task(title={self.title!r}, status={self.status.value}, priority={self.priority.name})"
