"""Read and write validated task records as UTF-8 JSON."""

import json
from pathlib import Path

from .tasks import Task, validate_title


def task_from_dict(record: dict) -> Task:
    """Validate persisted fields before constructing a task."""
    if not isinstance(record, dict):
        raise ValueError("Each task must be an object.")
    identifier = record.get("identifier")
    title = record.get("title")
    priority = record.get("priority")
    completed = record.get("completed")
    if (
        not isinstance(identifier, int)
        or isinstance(identifier, bool)
        or identifier < 1
    ):
        raise ValueError("Task identifiers must be positive integers.")
    if not isinstance(title, str):
        raise ValueError("Task titles must be strings.")
    if (
        not isinstance(priority, int)
        or isinstance(priority, bool)
        or priority not in (1, 2, 3)
    ):
        raise ValueError("Priority must be 1, 2, or 3.")
    if not isinstance(completed, bool):
        raise ValueError("Completion must be a boolean.")
    return Task(identifier, validate_title(title), priority, completed)


def load_tasks(path: Path) -> list[Task]:
    """Load task data, treating a missing file as an empty collection."""
    if not path.exists():
        return []
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("The task file must contain a JSON array.")
    tasks = [task_from_dict(record) for record in records]
    identifiers = [task.identifier for task in tasks]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Task identifiers must be unique.")
    return tasks


def save_tasks(path: Path, tasks: list[Task]) -> None:
    """Write a task collection with readable indentation and a final newline."""
    records = [task.to_dict() for task in tasks]
    contents = json.dumps(records, ensure_ascii=False, indent=2)
    path.write_text(contents + "\n", encoding="utf-8")
