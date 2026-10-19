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

class Task:
    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        self.validate_title(title)
        self.title = title
        self.description = description[:500] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if due_date:
            self.validate_due_date(due_date)

    @staticmethod
    def validate_title(title):
        if not title or len(title) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    def validate_due_date(self, due_date):
        if due_date < datetime.now():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True
        transitions = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
            TaskStatus.DONE: []
        }
        return new_status in transitions.get(self.status, [])

    def is_overdue(self):
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        if self.priority.value > other_task.priority.value:
            return 1
        elif self.priority.value < other_task.priority.value:
            return -1
        return 0