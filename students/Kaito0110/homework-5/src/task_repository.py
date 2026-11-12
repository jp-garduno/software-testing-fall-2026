
from src.task import Task


class TaskRepository:
    def __init__(self):
        self._tasks = {}

    def add(self, task: Task) -> Task:
        if task.task_id in self._tasks:
            raise ValueError("Task ID already exists")

        self._tasks[task.task_id] = task
        return task

    def get_by_id(self, task_id: int) -> Task:
        task = self._tasks.get(task_id)

        if task is None:
            raise KeyError("Task not found")

        return task

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, task: Task) -> Task:
        if task.task_id not in self._tasks:
            raise KeyError("Task not found")

        self._tasks[task.task_id] = task
        return task

    def delete(self, task_id: int) -> bool:
        if task_id not in self._tasks:
            raise KeyError("Task not found")

        del self._tasks[task_id]
        return True
