"""Task model for the TaskFlow task management system."""

import uuid
from datetime import datetime
from enum import Enum

TITLE_MIN_LENGTH = 3
TITLE_MAX_LENGTH = 100
DESCRIPTION_MAX_LENGTH = 500


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


# Forward-only transitions. ARCHIVED is reachable from every non-archived
# state and is handled separately in Task.can_transition.
_FORWARD_TRANSITIONS = {
    TaskStatus.TODO: TaskStatus.IN_PROGRESS,
    TaskStatus.IN_PROGRESS: TaskStatus.DONE,
}


class InvalidTransitionError(ValueError):
    """Raised when a status change does not follow the allowed paths."""


class Task:  # pylint: disable=too-many-instance-attributes
    """A unit of work with validation, a status lifecycle and a priority.

    The attributes are the seven fields the TaskFlow spec requires plus an id.
    """

    # `now` is injectable so creation-time validation is deterministic in tests.
    def __init__(  # pylint: disable=too-many-arguments
        self, title, description="", priority=TaskPriority.LOW, due_date=None, now=None
    ):
        now = now or datetime.now()
        self.validate_title(title)
        self.validate_description(description)
        if due_date is not None:
            self.validate_due_date(due_date, now)

        self.id = uuid.uuid4().hex
        self.title = title
        self.description = description or ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = now
        self.updated_at = now

    def __repr__(self):
        return f"Task(id={self.id!r}, title={self.title!r}, status={self.status.value}, priority={self.priority.name})"

    @staticmethod
    def validate_title(title):
        if not isinstance(title, str) or len(title.strip()) < TITLE_MIN_LENGTH:
            raise ValueError(f"Title must be at least {TITLE_MIN_LENGTH} characters")
        if len(title) > TITLE_MAX_LENGTH:
            raise ValueError(f"Title must not exceed {TITLE_MAX_LENGTH} characters")

    @staticmethod
    def validate_description(description):
        if description and len(description) > DESCRIPTION_MAX_LENGTH:
            raise ValueError(f"Description must not exceed {DESCRIPTION_MAX_LENGTH} characters")

    @staticmethod
    def validate_due_date(due_date, now=None):
        if due_date <= (now or datetime.now()):
            raise ValueError("Due date must be in the future")

    @property
    def is_archived(self):
        return self.status == TaskStatus.ARCHIVED

    def can_transition(self, new_status):
        """Return True if moving from the current status to new_status is allowed."""
        if self.is_archived:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        return _FORWARD_TRANSITIONS.get(self.status) == new_status

    def transition_to(self, new_status, now=None):
        """Change the status, raising InvalidTransitionError for a disallowed move."""
        if not self.can_transition(new_status):
            raise InvalidTransitionError(
                f"Invalid transition from {self.status.value} to {new_status.value}"
            )
        old_status = self.status
        self.status = new_status
        self.touch(now)
        return old_status

    def touch(self, now=None):
        self.updated_at = now or datetime.now()

    def is_overdue(self, now=None):
        """A task is overdue when its due date has passed and it is not DONE or ARCHIVED."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if self.due_date is None:
            return False
        return (now or datetime.now()) > self.due_date

    def compare_priority(self, other_task):
        """Return 1 if this task has higher priority, -1 if lower and 0 if equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0

    def __lt__(self, other):
        # Sorting a list of tasks puts the most urgent first.
        return self.compare_priority(other) > 0
