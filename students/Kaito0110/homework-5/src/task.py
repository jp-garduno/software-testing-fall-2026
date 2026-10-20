
from dataclasses import dataclass


@dataclass
class Task:
    task_id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "medium"

    def __post_init__(self):
        if self.task_id <= 0:
            raise ValueError("Task ID must be positive")

        if not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if self.priority not in ("low", "medium", "high"):
            raise ValueError("Invalid task priority")

    def mark_completed(self):
        self.completed = True

    def update_title(self, new_title: str):
        if not new_title.strip():
            raise ValueError("Task title cannot be empty")
        self.title = new_title
