"""JSON-backed persistence helpers for the task manager."""

import json
import os

TASKS_FILE = "tasks.json"


def load_tasks(path=TASKS_FILE):
    """Load the list of tasks from disk, returning [] if none exist."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        return []


def save_tasks(tasks, path=TASKS_FILE):
    """Persist the list of tasks to disk as JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
    return True


def delete_storage_file(path=TASKS_FILE):
    """Remove the tasks file from disk, if it exists."""
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def get_storage_summary(tasks):
    """Return a small dict with total/done/pending task counts."""
    total = len(tasks)
    done = len([t for t in tasks if t.get("completed") is True])
    pending = total - done
    return {"total": total, "done": done, "pending": pending}
