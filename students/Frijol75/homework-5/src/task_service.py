"""TaskService business logic layer orchestrating repository and notifications."""

from datetime import datetime
from typing import Any, List, Optional
from task import Task, TaskPriority, TaskStatus
from notification_service import NotificationService
from task_repository import TaskRepository


class TaskService:
    """Business logic for task operations, validation, and notification triggers."""

    def __init__(self, repository: TaskRepository, notification_service: NotificationService):
        self.repository = repository
        self.notification_service = notification_service

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: Optional[datetime] = None,
        recipient_email: str = "user@example.com",
    ) -> Task:
        """Create a new task with uniqueness validation and notification."""
        existing = self.repository.find_by_title(title)
        if existing:
            raise ValueError(f"Task with title '{title}' already exists")

        task = Task(title, description, priority, due_date)
        self.repository.save(task)

        try:
            self.notification_service.send_email(
                recipient_email,
                "New Task Created",
                f"Task '{title}' has been created",
            )
        except Exception:
            # External notification failure should not prevent task creation
            pass

        return task

    def create_task_with_sms(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: Optional[datetime] = None,
        phone_number: str = "1234567890",
        recipient_email: str = "user@example.com",
    ) -> Task:
        """Create task with both email and SMS notifications."""
        task = self.create_task(title, description, priority, due_date, recipient_email)
        try:
            self.notification_service.send_sms(
                phone_number,
                f"Urgent task created: {title}",
            )
        except Exception:
            pass
        return task

    def update_task_status(
        self,
        task_id: Any,
        new_status: TaskStatus,
        recipient_email: str = "user@example.com",
    ) -> Task:
        """Update task status with validation and notification."""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if not task.can_transition(new_status):
            old_str = task.status.value if hasattr(task.status, "value") else str(task.status)
            new_str = new_status.value if hasattr(new_status, "value") else str(new_status)
            raise ValueError(f"Invalid transition from {old_str} to {new_str}")

        old_status_val = task.status.value if hasattr(task.status, "value") else str(task.status)
        new_status_val = new_status.value if hasattr(new_status, "value") else str(new_status)

        task.status = new_status
        task.updated_at = datetime.now()
        self.repository.save(task)

        try:
            self.notification_service.send_email(
                recipient_email,
                "Task Status Updated",
                f"Task '{task.title}' changed from {old_status_val} to {new_status_val}",
            )
        except Exception:
            pass

        return task

    def update_task(
        self,
        task_id: Any,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        due_date: Optional[datetime] = None,
    ) -> Task:
        """Update task details with uniqueness check on title change."""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if title and title != task.title:
            existing = self.repository.find_by_title(title)
            if existing and getattr(existing, "id", None) != task_id:
                raise ValueError(f"Task with title '{title}' already exists")

        task.update(title=title, description=description, priority=priority, due_date=due_date)
        self.repository.save(task)
        return task

    def delete_task(self, task_id: Any, soft: bool = True) -> Any:
        """Delete task softly (mark ARCHIVED) or permanently remove from repository."""
        if soft:
            task = self.repository.find_by_id(task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            if task.status != TaskStatus.ARCHIVED:
                task.status = TaskStatus.ARCHIVED
                task.updated_at = datetime.now()
                self.repository.save(task)
            return task
        return self.repository.delete(task_id)

    def check_overdue_tasks(self, recipient_email: str = "user@example.com") -> List[Task]:
        """Check all tasks for overdue condition and dispatch notifications."""
        all_tasks = self.repository.find_all() or []
        overdue_tasks = [task for task in all_tasks if task.is_overdue()]

        for task in overdue_tasks:
            try:
                self.notification_service.send_email(
                    recipient_email,
                    "Task Overdue",
                    f"Task '{task.title}' is overdue!",
                )
            except Exception:
                pass

        return overdue_tasks

    def get_task(self, task_id: Any) -> Optional[Task]:
        """Retrieve task by identifier."""
        return self.repository.find_by_id(task_id)

    def search_tasks(
        self,
        query: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Task]:
        """Filter tasks using multiple search and filter parameters."""
        tasks = self.repository.find_all() or []

        if query:
            q_lower = query.lower()
            tasks = [
                t for t in tasks
                if q_lower in t.title.lower() or (t.description and q_lower in t.description.lower())
            ]

        if status:
            tasks = [t for t in tasks if t.status == status]

        if priority:
            tasks = [t for t in tasks if t.priority == priority]

        if start_date:
            tasks = [t for t in tasks if t.due_date and t.due_date >= start_date]

        if end_date:
            tasks = [t for t in tasks if t.due_date and t.due_date <= end_date]

        return tasks
