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


FORWARD_TRANSITIONS = {
    TaskStatus.TODO: TaskStatus.IN_PROGRESS,
    TaskStatus.IN_PROGRESS: TaskStatus.DONE,
}


class InvalidTransitionError(ValueError):
    """Raised when a status change does not follow TODO -> IN_PROGRESS -> DONE, or leaves ARCHIVED."""


class ArchivedTaskError(ValueError):
    """Raised when an archived task is edited."""


class Task:  # pylint: disable=too-many-instance-attributes
    """A unit of work with a validated title, a priority and a lifecycle that ends in ARCHIVED."""

    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        now = datetime.now()
        self.task_id = None
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.priority = self.validate_priority(priority)
        self.due_date = self.validate_due_date(due_date, now)
        self.status = TaskStatus.TODO
        self.created_at = now
        self.updated_at = now

    @staticmethod
    def validate_title(title):
        """Return the title without surrounding whitespace, or raise ValueError if it is not 3-100 characters."""
        cleaned = (title or "").strip()
        if not cleaned:
            raise ValueError("Title is required")
        if len(cleaned) < TITLE_MIN_LENGTH:
            raise ValueError(f"Title must be at least {TITLE_MIN_LENGTH} characters")
        if len(cleaned) > TITLE_MAX_LENGTH:
            raise ValueError(f"Title must not exceed {TITLE_MAX_LENGTH} characters")
        return cleaned

    @staticmethod
    def validate_description(description):
        """Return the description ("" when omitted), or raise ValueError if it exceeds 500 characters."""
        description = description or ""
        if len(description) > DESCRIPTION_MAX_LENGTH:
            raise ValueError(f"Description must not exceed {DESCRIPTION_MAX_LENGTH} characters")
        return description

    @staticmethod
    def validate_priority(priority):
        """Return the priority, or raise ValueError if it is not a TaskPriority."""
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be one of LOW, MEDIUM, HIGH or URGENT")
        return priority

    @staticmethod
    def validate_due_date(due_date, now):
        """Return the due date (None means no deadline), or raise ValueError if it is not later than now."""
        if due_date is not None and due_date <= now:
            raise ValueError("Due date must be in the future")
        return due_date

    def can_transition(self, new_status):
        """Return True when the lifecycle allows moving from the current status to new_status."""
        if self.status is TaskStatus.ARCHIVED:
            return False
        if new_status is TaskStatus.ARCHIVED:
            return True
        return FORWARD_TRANSITIONS.get(self.status) is new_status

    def transition_to(self, new_status):
        """Move to new_status and stamp updated_at, or raise InvalidTransitionError leaving the task unchanged."""
        if not self.can_transition(new_status):
            raise InvalidTransitionError(f"Cannot move a task from {self.status.value} to {new_status.value}")
        self.status = new_status
        self.updated_at = datetime.now()

    def update_details(self, *, title=None, description=None, priority=None, due_date=None):
        """Apply the given field changes all together, or none of them if any value is invalid.

        Fields left as None keep their value. Raises ArchivedTaskError for an archived task.
        """
        if self.status is TaskStatus.ARCHIVED:
            raise ArchivedTaskError("Archived tasks cannot be modified")
        now = datetime.now()
        changes = {}
        if title is not None:
            changes["title"] = self.validate_title(title)
        if description is not None:
            changes["description"] = self.validate_description(description)
        if priority is not None:
            changes["priority"] = self.validate_priority(priority)
        if due_date is not None:
            changes["due_date"] = self.validate_due_date(due_date, now)
        if not changes:
            return
        for field, value in changes.items():
            setattr(self, field, value)
        self.updated_at = now

    def is_overdue(self):
        """Return True when the due date has passed and the task is neither DONE nor ARCHIVED."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        """Return 1 if this task's priority is higher than other_task's, -1 if lower, 0 if equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0
