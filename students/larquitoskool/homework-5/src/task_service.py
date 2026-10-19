from datetime import datetime
from task import Task, TaskStatus, TaskPriority

class TaskService:
    def __init__(self, repository, notification_service):
        self.repository = repository
        self.notification_service = notification_service

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        if self.repository.find_by_title(title):
            raise ValueError(f"Task with title '{title}' already exists")
        task = Task(title, description, priority, due_date)
        self.repository.save(task)
        self.notification_service.send_email("user@example.com", "New Task Created", f"Task '{title}' has been created")
        return task

    def update_task_status(self, task_id, new_status):
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if not task.can_transition(new_status):
            raise ValueError(f"Invalid transition from {task.status} to {new_status}")
        
        old_status = task.status
        task.status = new_status
        task.updated_at = datetime.now()
        self.repository.save(task)
        self.notification_service.send_email("user@example.com", "Task Status Updated", f"Task '{task.title}' changed from {old_status} to {new_status}")
        return task

    def check_overdue_tasks(self):
        overdue_tasks = [t for t in self.repository.find_all() if t.is_overdue()]
        for task in overdue_tasks:
            self.notification_service.send_email("user@example.com", "Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue_tasks