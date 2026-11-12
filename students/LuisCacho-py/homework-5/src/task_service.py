"""Business logic layer for task management."""

from datetime import datetime
from src.task import Task, TaskPriority, TaskStatus


class TaskService:
    """Business logic layer for task management."""

    def __init__(self, repository, notification_service):
        self.repository = repository
        self.notification_service = notification_service

    def _notify_email(self, subject, body):
        """Send email notification without breaking workflow if external service fails."""
        try:
            self.notification_service.send_email("user@example.com", subject, body)
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a new task with validation and notification."""
        existing = self.repository.find_by_title(title)
        if existing:
            raise ValueError(f"Task with title '{title}' already exists")

        task = Task(title, description, priority, due_date)
        self.repository.save(task)

        self._notify_email("New Task Created", f"Task '{title}' has been created")
        if priority == TaskPriority.URGENT:
            self.notification_service.send_sms("+15550001234", f"Urgent task '{title}' created")

        return task

    def update_task_status(self, task_id, new_status):
        """Update task status with validation and notification."""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if not task.can_transition(new_status):
            raise ValueError(f"Invalid transition from {task.status} to {new_status}")

        old_status = task.status
        task.status = new_status
        task.updated_at = datetime.now()

        self.repository.save(task)
        self._notify_email(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status} to {new_status}",
        )
        return task

    def delete_task(self, task_id):
        """Soft delete a task by marking it as ARCHIVED."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def check_overdue_tasks(self):
        """Check for overdue tasks and send notifications."""
        all_tasks = self.repository.find_all()
        overdue_tasks = [task for task in all_tasks if task.is_overdue()]

        for task in overdue_tasks:
            self._notify_email("Task Overdue", f"Task '{task.title}' is overdue!")

        return overdue_tasks

    def search_tasks(self, status=None, priority=None, title_query=None):
        """Search and filter tasks by status, priority, and partial title match."""
        tasks = self.repository.find_all()
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        if title_query is not None:
            tasks = [t for t in tasks if title_query.lower() in t.title.lower()]
        return tasks
