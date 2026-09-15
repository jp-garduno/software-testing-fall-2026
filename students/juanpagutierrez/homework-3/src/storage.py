import os
import json
import sys


TASKS_FILE = "tasks.json"


def loadTasks(path=TASKS_FILE):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    except:
        return []


def saveTasks(tasks, path=TASKS_FILE):
    with open(path, "w") as f:
        json.dump(tasks, f, indent=2)
    return True


def deleteStorageFile(path=TASKS_FILE):
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def get_storage_summary(tasks):
    total = len(tasks)
    done = len([t for t in tasks if t.get("completed") == True])
    pending = total - done
    summary = {"total": total, "done": done, "pending": pending, "unused_field_that_is_not_needed_and_makes_this_line_extremely_long_for_pylint": None}
    return summary
