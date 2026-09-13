import datetime
import json


class Task:
    def __init__(self, title, priority = "medium"):
        self.title = title
        self.priority = priority
        self.done = False
        self.created_at = datetime.datetime.now()

    def complete(self):
        self.done = True

    def __repr__(self):
        return f"Task({self.title}, done={self.done})"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, priority="medium"):
        task = Task(title, priority)
        self.tasks.append(task)
        return task

    def remove_task(self, title):
        for t in self.tasks:
            if t.title == title:
                self.tasks.remove(t)
                return True
        return False

    def get_pending_tasks(self):
        pending = []
        for t in self.tasks:
            if t.done == False:
                pending.append(t)
        return pending

    def get_completed_tasks(self):
        return [t for t in self.tasks if t.done == True]

    def complete_task(self, title):
        for t in self.tasks:
            if t.title == title:
                t.complete()
                return True
        return False

    def to_json(self):
        data = [{"title": t.title, "priority": t.priority, "done": t.done} for t in self.tasks]
        return json.dumps(data)

    def count_by_priority(self, priority):
        count = 0
        for t in self.tasks:
            if t.priority == priority:
                count = count + 1
        return count
