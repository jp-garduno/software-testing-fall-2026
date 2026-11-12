"""Task domain model and state-management rules for TaskFlow."""

from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Lifecycle states for a task."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    """Priority levels in ascending importance."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Task:
    """A validated task with lifecycle and priority behavior."""

    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a task in TODO status."""
        self.validate_title(title)
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority")
        if due_date:
            self.validate_due_date(due_date)

        self.id = None
        self.title = title
        self.description = description[:500] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @staticmethod
    def validate_title(title):
        """Validate the required title length."""
        if not title or len(title) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_due_date(due_date):
        """Reject due dates in the past."""
        if due_date <= datetime.now():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        """Return whether a lifecycle change respects the transition graph."""
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
        """Return true only for unfinished tasks whose due date has passed."""
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        return bool(self.due_date and datetime.now() > self.due_date)

    def compare_priority(self, other_task):
        """Compare this task priority to another task."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0
