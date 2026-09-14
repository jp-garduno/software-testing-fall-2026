from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(str, Enum):
    OPEN = "open"
    COMPLETED = "completed"


@dataclass
class Task:
    identifier: int
    title: str
    priority: int
    tags: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.OPEN

    @property
    def is_completed(self) -> bool:
        return self.status is TaskStatus.COMPLETED

    def mark_complete(self) -> None:
        self.status = TaskStatus.COMPLETED

    def reopen(self) -> None:
        self.status = TaskStatus.OPEN

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.identifier,
            "title": self.title,
            "priority": self.priority,
            "tags": list(self.tags),
            "status": self.status.value,
        }
