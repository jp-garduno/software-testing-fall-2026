"""Domain model for TaskFlow."""
from datetime import datetime
from enum import Enum


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


MIN_TITLE_LENGTH = 3
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500

_TRANSITIONS = {
    TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
    TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
    TaskStatus.DONE: [],
}


class Task:
    def __init__(self, title, description="", priority=TaskPriority.LOW,
                 due_date=None, task_id=None):
        self.validate_title(title)
        if due_date is not None:
            self.validate_due_date(due_date)

        self.id = task_id
        self.title = title
        self.description = description[:MAX_DESCRIPTION_LENGTH] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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

    def can_transition(self, new_status):
        """ARCHIVED is terminal; any other state may go to ARCHIVED."""
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        return new_status in _TRANSITIONS.get(self.status, [])

    def is_overdue(self):
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        """Return 1 if higher, -1 if lower, 0 if equal."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0