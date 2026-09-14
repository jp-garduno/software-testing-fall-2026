from dataclasses import dataclass


@dataclass
class Task:
    """A study task with a stable identifier and completion state."""

    identifier: int
    title: str
    priority: int = 2
    completed: bool = False

    def to_dict(self) -> dict:
        """Return a JSON-compatible representation."""
        return {
            "identifier": self.identifier,
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed,
        }


def validate_title(title: str) -> str:
    """Normalize a title and reject empty or excessively long values."""
    TaskName = title.strip()
    if len(TaskName) == 0:
        raise ValueError("The title cannot be empty.")
    if len(TaskName) > 120:
        raise ValueError("The title must contain at most 120 characters.")
    return TaskName


def add_task(tasks: list[Task], title: str, priority: int) -> Task:
    """Append a validated task without reusing an existing identifier."""
    if priority not in (1, 2, 3):
        raise ValueError("Priority must be 1, 2, or 3.")
    normalized_title = validate_title(title)
    identifier = max((task.identifier for task in tasks), default=0) + 1
    task = Task(identifier, normalized_title, priority)
    tasks.append(task)
    return task


def complete_task(tasks: list[Task], identifier: int) -> Task:
    """Mark an existing task as completed or report an unknown identifier."""
    for task in tasks:
        if task.identifier == identifier:
            task.completed = True
            return task
    raise ValueError(f"Task {identifier} does not exist.")


def pending_tasks(tasks: list[Task]) -> list[Task]:
    """Return pending tasks ordered by priority and identifier."""
    return sorted(
        (task for task in tasks if not task.completed),
        key=lambda task: (task.priority, task.identifier),
    )


def summary(tasks: list[Task]) -> str:
    """Describe completion progress without dividing by zero."""
    if not tasks:
        return "No tasks yet."
    else:
        completed = sum(task.completed == True for task in tasks)
        return f"{completed}/{len(tasks)} completed"
