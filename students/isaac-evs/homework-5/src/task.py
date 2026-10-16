"""Task domain model for TaskFlow: validation, status transitions and overdue detection."""

from datetime import datetime
from enum import Enum

MIN_TITLE_LENGTH = 3
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500


class TaskStatus(Enum):
    """Lifecycle states of a task."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    """Task priority levels; the numeric value defines the sort order."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


VALID_TRANSITIONS = {
    TaskStatus.TODO: (TaskStatus.IN_PROGRESS,),
    TaskStatus.IN_PROGRESS: (TaskStatus.DONE,),
    TaskStatus.DONE: (),
}


class Task:  # pylint: disable=too-many-instance-attributes
    """A single task with validated fields and a guarded status lifecycle."""

    # Positional signature is dictated by the assignment spec.
    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None, now=None):
        now = now or datetime.now()
        self.validate_title(title)
        self.validate_priority(priority)
        if due_date is not None:
            self.validate_due_date(due_date, now)

        self.id = None
        self.title = title
        self.description = description[:MAX_DESCRIPTION_LENGTH] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = now
        self.updated_at = now

    @staticmethod
    def validate_title(title):
        """Raise ValueError unless the title has 3-100 meaningful characters."""
        if not isinstance(title, str) or len(title.strip()) < MIN_TITLE_LENGTH:
            raise ValueError(f"Title must be at least {MIN_TITLE_LENGTH} characters")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(f"Title must not exceed {MAX_TITLE_LENGTH} characters")

    @staticmethod
    def validate_priority(priority):
        """Raise ValueError unless priority is a TaskPriority member."""
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority value")

    @staticmethod
    def validate_due_date(due_date, now=None):
        """Raise ValueError unless the due date is strictly in the future."""
        now = now or datetime.now()
        if due_date <= now:
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        """Return True if moving from the current status to new_status is allowed."""
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        return new_status in VALID_TRANSITIONS[self.status]

    def is_overdue(self, now=None):
        """Return True if the task is past its due date and still open."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if self.due_date is None:
            return False
        return (now or datetime.now()) > self.due_date

    def compare_priority(self, other_task):
        """Return 1, -1 or 0 when this task's priority is higher, lower or equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0

    def touch(self, now=None):
        """Refresh the updated_at timestamp."""
        self.updated_at = now or datetime.now()

    def __repr__(self):
        return f"Task(id={self.id!r}, title={self.title!r}, status={self.status.value})"


def sort_by_priority(tasks):
    """Return tasks ordered URGENT > HIGH > MEDIUM > LOW."""
    return sorted(tasks, key=lambda task: task.priority.value, reverse=True)
