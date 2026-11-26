import json
import os
from models import Task, TaskList

DEFAULT_PATH = "tasks.json"


def save_tasks(task_list, path=DEFAULT_PATH):
    data = [t.to_dict() for t in task_list.tasks]
    f = open(path, "w")
    json.dump(data, f, indent=2)
    f.close()


def load_tasks(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return TaskList([])
    with open(path, "r") as f:
        raw = json.load(f)
    tasks = []
    for item in raw:
        tasks.append(Task.from_dict(item))
    return TaskList(tasks)


def export_summary(task_list, path="summary.txt"):
    pending = task_list.get_pending()
    done = task_list.get_done()
    with open(path, "w") as f:
        f.write("Pending tasks: " + str(len(pending)) + "\n")
        for t in pending:
            f.write("- " + t.title + "\n")
        f.write("\nDone tasks: " + str(len(done)) + "\n")
        for t in done:
            f.write("- " + t.title + "\n")


def backup_exists(path=DEFAULT_PATH):
    backup_path = path + ".bak"
    return os.path.exists(backup_path)
