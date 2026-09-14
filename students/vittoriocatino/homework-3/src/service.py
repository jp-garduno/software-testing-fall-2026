from .models import Task
from .validation import normalise_tags, validate_priority, validate_title


class TaskService:
    def __init__(self) -> None:
        self._tasks = {}
        self._next_identifier = 1

    def create_task(self, title: str, priority: int = 3, tags: list[str] | None = None) -> Task:
        task = Task(
            identifier=self._next_identifier,
            title=validate_title(title),
            priority=validate_priority(priority),
            tags=normalise_tags(tags),
        )
        self._tasks[task.identifier] = task
        self._next_identifier += 1
        return task

    def get_task(self, identifier: int) -> Task:
        try:
            return self._tasks[identifier]
        except KeyError as error:
            raise KeyError(f"Task {identifier} does not exist") from error

    def complete_task(self, identifier: int) -> Task:
        task = self.get_task(identifier)
        task.mark_complete()
        return task

    def reopen_task(self, identifier: int) -> Task:
        task = self.get_task(identifier)
        task.reopen()
        return task

    def update_priority(self, identifier: int, priority: int) -> Task:
        task = self.get_task(identifier)
        task.priority = validate_priority(priority)
        return task

    def remove_task(self, identifier: int) -> Task:
        task = self.get_task(identifier)
        del self._tasks[identifier]
        return task

    def list_tasks(self, completed: bool | None = None) -> list[Task]:
        tasks = list(self._tasks.values())
        if completed is None:
            return tasks
        return [task for task in tasks if task.is_completed is completed]

    def summary(self) -> dict[str, int]:
        all_tasks = self.list_tasks()
        completed_count = len(self.list_tasks(completed=True))
        return {
            "total": len(all_tasks),
            "completed": completed_count,
            "open": len(all_tasks) - completed_count,
        }
