"""Task data, lifecycle rules and time-based behavior."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from uuid import uuid4


def utc_now() -> datetime:
    """Return the current UTC instant; callers can inject a different clock."""
    return datetime.now(timezone.utc)


def as_utc(value: datetime) -> datetime:
    """Normalize a datetime to UTC, treating a naive input as UTC."""
    if not isinstance(value, datetime):
        raise ValueError("Expected a datetime")
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class TaskStatus(Enum):
    """The four states in the task lifecycle."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(IntEnum):
    """Priority values increase with urgency."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


# Required domain fields plus an injectable clock form one cohesive data model.
@dataclass
class Task:  # pylint: disable=too-many-instance-attributes
    """A task with an automatically assigned identity and timestamps."""

    title: str
    description: str | None = ""
    priority: TaskPriority = TaskPriority.LOW
    due_date: datetime | None = None
    clock: Callable[[], datetime] = field(
        default=utc_now, repr=False, compare=False, kw_only=True
    )
    id: str = field(init=False)
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.validate_title(self.title)
        self.description = self.validate_description(self.description)
        self.validate_priority(self.priority)
        self.id = str(uuid4())
        self.created_at = as_utc(self.clock())
        self.updated_at = self.created_at
        if self.due_date is not None:
            self.due_date = self.validate_due_date(self.due_date, now=self.created_at)

    @staticmethod
    def validate_title(title: str) -> None:
        """Require a nonblank string containing between 3 and 100 characters."""
        if (
            not isinstance(title, str)
            or not title.strip()
            or not 3 <= len(title) <= 100
        ):
            raise ValueError("Title must contain 3 to 100 characters and not be blank")

    @staticmethod
    def validate_description(description: str | None) -> str:
        """Normalize an omitted description and reject oversized or nonstring data."""
        if description is None:
            return ""
        if not isinstance(description, str) or len(description) > 500:
            raise ValueError("Description must be a string of at most 500 characters")
        return description

    @staticmethod
    def validate_priority(priority: TaskPriority) -> None:
        """Accept only one of the declared priority levels."""
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority")

    def validate_due_date(
        self, due_date: datetime, *, now: datetime | None = None
    ) -> datetime:
        """Return a UTC due date strictly later than the supplied or current instant."""
        normalized = as_utc(due_date)
        current = as_utc(self.clock()) if now is None else as_utc(now)
        if normalized <= current:
            raise ValueError("Due date must be in the future")
        return normalized

    def can_transition(self, new_status: TaskStatus) -> bool:
        """Allow forward lifecycle steps and archiving, with ARCHIVED terminal."""
        if self.status is TaskStatus.ARCHIVED or not isinstance(new_status, TaskStatus):
            return False
        if new_status is TaskStatus.ARCHIVED:
            return True
        transitions = {
            TaskStatus.TODO: (TaskStatus.IN_PROGRESS,),
            TaskStatus.IN_PROGRESS: (TaskStatus.DONE,),
            TaskStatus.DONE: (),
        }
        return new_status in transitions[self.status]

    def is_overdue(self) -> bool:
        """Only unfinished, unarchived tasks with past due dates are overdue."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        return self.due_date is not None and as_utc(self.clock()) > self.due_date

    def compare_priority(self, other_task: "Task") -> int:
        """Return 1, -1 or 0 when this priority is higher, lower or equal."""
        if self.priority > other_task.priority:
            return 1
        if self.priority < other_task.priority:
            return -1
        return 0
