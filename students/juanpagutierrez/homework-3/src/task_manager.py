import datetime
from storage import loadTasks, saveTasks


PRIORITY_LEVELS = ["low", "medium", "high"]


class TaskManager:
    def __init__(self, tasks=[]):
        self.tasks = tasks if tasks else loadTasks()
        self.next_id = len(self.tasks) + 1

    def add_task(self, title, priority="medium", due_date=None):
        if priority not in PRIORITY_LEVELS: priority = "medium"
        task = {
            "id": self.next_id,
            "title": title,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": str(datetime.datetime.now()),
        }
        self.tasks.append(task)
        self.next_id += 1
        saveTasks(self.tasks)
        return task

    def complete_task(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = True
                saveTasks(self.tasks)
                return True
        return False

    def remove_task(self, task_id):
        found = False
        for t in self.tasks:
            if t["id"] == task_id:
                found = True
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        saveTasks(self.tasks)
        return found

    def list_tasks(self, show_completed=True, filter_priority=None):
        result = []
        for t in self.tasks:
            if not show_completed and t["completed"]:
                continue
            if filter_priority is not None and t["priority"] != filter_priority:
                continue
            result.append(t)
        return result

    def get_tasks_sorted_by_priority_and_then_by_creation_date_descending(self):
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.tasks, key=lambda t: (order[t["priority"]], t["created_at"]))
