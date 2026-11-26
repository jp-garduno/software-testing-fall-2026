import os
import sys
import datetime


class Task:
    def __init__(self,title,description="",done=False,priority=2):
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.created_at = datetime.datetime.now()

    def mark_done(self):
        self.done = True

    def mark_pending(self):
        self.done=False

    def toggle(self):
        if self.done == True:
            self.done = False
        else:
            self.done = True

    def is_high_priority(self):
        return self.priority==1

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        t = Task(data["title"], data["description"], data["done"], data["priority"])
        return t

    def __repr__(self):
        status = "x" if self.done else " "
        return f"[{status}] {self.title} (priority={self.priority})"


class TaskList:
    def __init__(self, tasks=[]):
        self.tasks = tasks

    def add(self, task):
        self.tasks.append(task)

    def remove(self, index):
        del self.tasks[index]

    def get_pending(self):
        result = []
        for t in self.tasks:
            if not t.done:
                result.append(t)
        return result

    def get_done(self):
        return [t for t in self.tasks if t.done]

    def sort_by_priority(self):
        self.tasks.sort(key=lambda t: t.priority)

    def count(self):
        return len(self.tasks)

    def clear_completed(self):
        self.tasks = [t for t in self.tasks if t.done == False]
