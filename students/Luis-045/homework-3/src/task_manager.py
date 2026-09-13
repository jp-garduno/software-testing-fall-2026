from src.task import Task


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description="", priority="medium"):
        task = Task(title, description, priority)
        self.tasks.append(task)
        return task

    def find_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def complete_task(self, title):
        task = self.find_task(title)
        if task is None:
            return False
        task.mark_completed()
        return True

    def remove_task(self, title):
        task = self.find_task(title)
        if task is None:
            return False
        self.tasks.remove(task)
        return True

    def change_priority(self, title, priority):
        task = self.find_task(title)
        if task is None:
            return False
        task.update_priority(priority)
        return True

    def pending_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def completed_tasks(self):
        return [task for task in self.tasks if task.completed]

    def count_tasks(self):
        return len(self.tasks)

    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task.completed]

    def tasks_by_priority(self, priority):
        return [task for task in self.tasks if task.priority == priority]

    def completion_percentage(self):
        if not self.tasks:
            return 0.0

        total_tasks = len(self.tasks)
        completed_tasks = len(self.completed_tasks())
        completion_ratio = completed_tasks / total_tasks
        percentage = completion_ratio * 100

        return percentage

    def summary(self):
        total = self.count_tasks()
        completed = len(self.completed_tasks())
        pending = len(self.pending_tasks())

        return (
            f"Task summary -> total tasks: {total}, "
            f"completed tasks: {completed}, "
            f"pending tasks: {pending}, "
            "completion tracking enabled"
        )
