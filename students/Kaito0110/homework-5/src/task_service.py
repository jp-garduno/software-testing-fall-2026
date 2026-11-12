
from src.task import Task
from src.task_repository import TaskRepository
from src.notification_service import NotificationService


class TaskService:
    def __init__(self, repository=None, notifications=None):
        self.repository = repository or TaskRepository()
        self.notifications = notifications or NotificationService()

    def create_task(
        self,
        task_id: int,
        title: str,
        description: str = "",
        priority: str = "medium",
    ) -> Task:
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
        )
        self.repository.add(task)
        self.notifications.send_task_created(task)
        return task

    def get_task(self, task_id: int) -> Task:
        return self.repository.get_by_id(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.get_all()

    def complete_task(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        task.mark_completed()
        self.repository.update(task)
        self.notifications.send_task_completed(task)
        return task

    def update_task_title(self, task_id: int, new_title: str) -> Task:
        task = self.repository.get_by_id(task_id)
        task.update_title(new_title)
        self.repository.update(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)
