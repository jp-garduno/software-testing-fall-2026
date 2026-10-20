"""Task model with explicit validation and a replaceable local clock."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Callable
from uuid import uuid4


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    title: str
    description: str = ""
    priority: TaskPriority = TaskPriority.LOW
    due_date: datetime | None = None
    clock: Callable[[], datetime] = field(default=datetime.now, repr=False, compare=False)
    id: str = field(default_factory=lambda: str(uuid4()), init=False)
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)

    def __post_init__(self):
        self.validate_title(self.title)
        self.validate_description(self.description)
        self.validate_priority(self.priority)
        self.validate_due_date(self.due_date)
        self.created_at = self.updated_at = self.clock()

    @staticmethod
    def validate_title(title):
        if not isinstance(title, str) or not 3 <= len(title) <= 100:
            raise ValueError("Title must contain 3-100 characters")
        if not title.strip():
            raise ValueError("Title cannot be blank")

    @staticmethod
    def validate_description(description):
        if not isinstance(description, str) or len(description) > 500:
            raise ValueError("Description must be a string of at most 500 characters")

    @staticmethod
    def validate_priority(priority):
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority")

    def validate_due_date(self, due_date):
        if due_date is None:
            return
        if not isinstance(due_date, datetime) or due_date.tzinfo is not None:
            raise ValueError("Due date must be a naive local datetime")
        if due_date <= self.clock():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        transitions = {
            TaskStatus.TODO: (TaskStatus.IN_PROGRESS, TaskStatus.ARCHIVED),
            TaskStatus.IN_PROGRESS: (TaskStatus.DONE, TaskStatus.ARCHIVED),
            TaskStatus.DONE: (TaskStatus.ARCHIVED,),
            TaskStatus.ARCHIVED: (),
        }
        return new_status in transitions[self.status]

    def is_overdue(self):
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        return self.due_date is not None and self.due_date < self.clock()

    def compare_priority(self, other_task):
        return (self.priority > other_task.priority) - (self.priority < other_task.priority)
