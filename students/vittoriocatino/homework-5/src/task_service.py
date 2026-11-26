"""TaskFlow business workflows coordinated across repository and notifications."""

from datetime import datetime

from task import Task, TaskPriority, TaskStatus


class TaskService:
    """Business logic for task creation, updates, state changes, and searches."""

    def __init__(self, repository, notification_service):
        """Create the service with its database and messaging boundaries."""
        self.repository = repository
        self.notification_service = notification_service

    def _notify(self, subject, body, urgent=False):
        """Attempt notifications without letting provider failure break workflows."""
        try:
            self.notification_service.send_email("user@example.com", subject, body)
            if urgent:
                self.notification_service.send_sms("+15550000000", body)
        except Exception:
            return False
        return True

    def create_task(
        self, title, description="", priority=TaskPriority.LOW, due_date=None
    ):
        """Create, persist, and notify about a task after duplicate validation."""
        if self.repository.find_by_title(title):
            raise ValueError(f"Task with title '{title}' already exists")
        task = Task(title, description, priority, due_date)
        self.repository.save(task)
        self._notify(
            "New Task Created",
            f"Task '{title}' has been created",
            urgent=priority == TaskPriority.URGENT,
        )
        return task

    def update_task_status(self, task_id, new_status):
        """Apply a valid status transition, persist it, and notify the user."""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if not task.can_transition(new_status):
            raise ValueError(f"Invalid transition from {task.status} to {new_status}")
        old_status = task.status
        task.status = new_status
        task.updated_at = datetime.now()
        self.repository.save(task)
        self._notify(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return task

    def update_task(self, task_id, **changes):
        """Update editable task fields while enforcing validation and uniqueness."""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if task.status == TaskStatus.ARCHIVED:
            raise ValueError("Archived tasks cannot be modified")
        if "title" in changes and changes["title"] != task.title:
            Task.validate_title(changes["title"])
            if self.repository.find_by_title(changes["title"]):
                raise ValueError(f"Task with title '{changes['title']}' already exists")
        if "due_date" in changes and changes["due_date"]:
            Task.validate_due_date(changes["due_date"])
        for field in ("title", "description", "priority", "due_date"):
            if field in changes:
                value = changes[field]
                if field == "description":
                    value = value[:500] if value else ""
                if field == "priority" and not isinstance(value, TaskPriority):
                    raise ValueError("Priority must be a TaskPriority")
                setattr(task, field, value)
        task.updated_at = datetime.now()
        self.repository.save(task)
        return task

    def delete_task(self, task_id):
        """Soft-delete a task by moving it to its terminal archived state."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def check_overdue_tasks(self):
        """Find overdue tasks and attempt one notification per overdue task."""
        overdue_tasks = [
            task for task in self.repository.find_all() if task.is_overdue()
        ]
        for task in overdue_tasks:
            self._notify("Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue_tasks

    def search_tasks(
        self, status=None, priority=None, start_date=None, end_date=None, title=None
    ):
        """Filter repository tasks by lifecycle, priority, dates, and partial title."""
        results = self.repository.find_all()
        if status:
            results = [task for task in results if task.status == status]
        if priority:
            results = [task for task in results if task.priority == priority]
        if start_date:
            results = [
                task
                for task in results
                if task.due_date and task.due_date >= start_date
            ]
        if end_date:
            results = [
                task for task in results if task.due_date and task.due_date <= end_date
            ]
        if title:
            query = title.lower()
            results = [task for task in results if query in task.title.lower()]
        return results
