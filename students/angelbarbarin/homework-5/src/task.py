"""Task model for TaskFlow: data, validation, status transitions and priority."""

from __future__ import annotations

import uuid
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
    """Priority levels; the value is the sort weight (URGENT > HIGH > MEDIUM > LOW)."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


# Forward-only transitions. ARCHIVED is reachable from every non-terminal state
# and is handled separately in Task.can_transition.
VALID_TRANSITIONS: dict[TaskStatus, tuple[TaskStatus, ...]] = {
    TaskStatus.TODO: (TaskStatus.IN_PROGRESS,),
    TaskStatus.IN_PROGRESS: (TaskStatus.DONE,),
    TaskStatus.DONE: (),
    TaskStatus.ARCHIVED: (),
}


class TaskValidationError(ValueError):
    """Raised when a task field breaks a validation rule."""


class InvalidTransitionError(ValueError):
    """Raised when a status change does not follow the allowed transitions."""


class Task:  # pylint: disable=too-many-instance-attributes
    """A single unit of work with a title, priority, due date and status."""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: datetime | None = None,
    ) -> None:
        self.validate_title(title)
        self.validate_description(description)
        self.validate_priority(priority)
        if due_date is not None:
            self.validate_due_date(due_date)

        now = datetime.now()
        self.id = uuid.uuid4().hex
        self.title = title
        self.description = description or ""
        self.priority = priority
        self.due_date = due_date
        self.status = TaskStatus.TODO
        self.created_at = now
        self.updated_at = now

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #
    @staticmethod
    def validate_title(title: str) -> None:
        """Title is required and must be 3-100 characters (surrounding spaces ignored)."""
        if not isinstance(title, str) or not title.strip():
            raise TaskValidationError("Title is required")
        length = len(title.strip())
        if length < TITLE_MIN_LENGTH:
            raise TaskValidationError(f"Title must be at least {TITLE_MIN_LENGTH} characters")
        if length > TITLE_MAX_LENGTH:
            raise TaskValidationError(f"Title must not exceed {TITLE_MAX_LENGTH} characters")

    @staticmethod
    def validate_description(description: str | None) -> None:
        """Description is optional but limited to 500 characters."""
        if description is None:
            return
        if not isinstance(description, str):
            raise TaskValidationError("Description must be a string")
        if len(description) > DESCRIPTION_MAX_LENGTH:
            raise TaskValidationError(f"Description must not exceed {DESCRIPTION_MAX_LENGTH} characters")

    @staticmethod
    def validate_priority(priority: TaskPriority) -> None:
        """Priority must be one of the TaskPriority members."""
        if not isinstance(priority, TaskPriority):
            raise TaskValidationError(f"Invalid priority: {priority!r}")

    @staticmethod
    def validate_due_date(due_date: datetime) -> None:
        """Due date must be a datetime in the future."""
        if not isinstance(due_date, datetime):
            raise TaskValidationError("Due date must be a datetime")
        if due_date <= datetime.now():
            raise TaskValidationError("Due date must be in the future")

    # ------------------------------------------------------------------ #
    # Status transitions
    # ------------------------------------------------------------------ #
    def can_transition(self, new_status: TaskStatus) -> bool:
        """Return True when moving from the current status to new_status is allowed."""
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        return new_status in VALID_TRANSITIONS[self.status]

    def transition_to(self, new_status: TaskStatus) -> TaskStatus:
        """Change the status if the transition is valid. Returns the previous status."""
        if not isinstance(new_status, TaskStatus):
            raise InvalidTransitionError(f"Unknown status: {new_status!r}")
        if not self.can_transition(new_status):
            raise InvalidTransitionError(f"Invalid transition from {self.status.value} to {new_status.value}")
        old_status = self.status
        self.status = new_status
        self.touch()
        return old_status

    @property
    def is_archived(self) -> bool:
        """True once the task reached the terminal ARCHIVED state."""
        return self.status == TaskStatus.ARCHIVED

    # ------------------------------------------------------------------ #
    # Field updates
    # ------------------------------------------------------------------ #
    def update_fields(
        self,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        due_date: datetime | None = None,
    ) -> list[str]:
        """Validate and apply the given fields. Returns the names of the fields that changed.

        All values are validated before anything is written, so a bad value leaves the
        task untouched. Archived tasks cannot be modified.
        """
        if self.is_archived:
            raise InvalidTransitionError("Archived tasks cannot be modified")

        changes: dict[str, object] = {}
        if title is not None:
            self.validate_title(title)
            changes["title"] = title
        if description is not None:
            self.validate_description(description)
            changes["description"] = description
        if priority is not None:
            self.validate_priority(priority)
            changes["priority"] = priority
        if due_date is not None:
            self.validate_due_date(due_date)
            changes["due_date"] = due_date

        changed = [name for name, value in changes.items() if getattr(self, name) != value]
        for name in changed:
            setattr(self, name, changes[name])
        if changed:
            self.touch()
        return changed

    def touch(self) -> None:
        """Refresh updated_at."""
        self.updated_at = datetime.now()

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #
    def is_overdue(self, now: datetime | None = None) -> bool:
        """Overdue when the due date has passed and the task is neither DONE nor ARCHIVED."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if self.due_date is None:
            return False
        current = now or datetime.now()
        return self.due_date < current

    def compare_priority(self, other: Task) -> int:
        """Return 1 if this task has higher priority, -1 if lower, 0 if equal."""
        if self.priority.value > other.priority.value:
            return 1
        if self.priority.value < other.priority.value:
            return -1
        return 0

    def __lt__(self, other: Task) -> bool:
        """Lower priority sorts first; use sorted(..., reverse=True) for URGENT first."""
        return self.compare_priority(other) < 0

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, status={self.status.value}, priority={self.priority.name})"
