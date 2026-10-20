"""Business logic layer for TaskFlow."""
import logging
from datetime import datetime

from task import MAX_DESCRIPTION_LENGTH, Task, TaskPriority, TaskStatus

logger = logging.getLogger(__name__)

DEFAULT_RECIPIENT = "user@example.com"
DEFAULT_PHONE = "+520000000000"


class TaskService:
    def __init__(self, repository, notification_service):
        self.repository = repository
        self.notification_service = notification_service

    # ---------- helpers ----------
    def _get_task(self, task_id):
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    def _safe_send(self, send, *args):
        """Notification failures must never break the main workflow."""
        try:
            send(*args)
            return True
        except Exception as exc:
            logger.warning("Notification failed: %s", exc)
            return False

    def _notify(self, subject, body):
        return self._safe_send(
            self.notification_service.send_email, DEFAULT_RECIPIENT, subject, body
        )

    # ---------- create ----------
    def create_task(self, title, description="", priority=TaskPriority.LOW,
                    due_date=None):
        if self.repository.find_by_title(title):
            raise ValueError(f"Task with title '{title}' already exists")

        task = Task(title, description, priority, due_date)
        self.repository.save(task)
        self._notify("New Task Created", f"Task '{title}' has been created")
        return task

    def create_task_with_sms(self, title, description="",
                             priority=TaskPriority.LOW, due_date=None):
        task = self.create_task(title, description, priority, due_date)
        if priority == TaskPriority.URGENT:
            self._safe_send(
                self.notification_service.send_sms,
                DEFAULT_PHONE, f"URGENT task created: {title}",
            )
        return task

    # ---------- update ----------
    def update_task_status(self, task_id, new_status):
        task = self._get_task(task_id)
        if not task.can_transition(new_status):
            raise ValueError(
                f"Invalid transition from {task.status.value} to {new_status.value}"
            )

        old_status = task.status
        task.status = new_status
        task.updated_at = datetime.now()
        self.repository.save(task)
        self._notify(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return task

    def update_task(self, task_id, title=None, description=None,
                    priority=None, due_date=None):
        task = self._get_task(task_id)
        if task.status == TaskStatus.ARCHIVED:
            raise ValueError("Cannot modify an archived task")

        # Validate everything first so a failure never leaves a half-updated task
        if title is not None:
            Task.validate_title(title)
            existing = self.repository.find_by_title(title)
            if existing is not None and existing is not task:
                raise ValueError(f"Task with title '{title}' already exists")
        if due_date is not None:
            Task.validate_due_date(due_date)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description[:MAX_DESCRIPTION_LENGTH]
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date

        task.updated_at = datetime.now()
        self.repository.save(task)
        return task

    # ---------- delete (soft) ----------
    def delete_task(self, task_id):
        task = self._get_task(task_id)
        if task.status == TaskStatus.ARCHIVED:
            raise ValueError("Task is already archived")

        task.status = TaskStatus.ARCHIVED
        task.updated_at = datetime.now()
        self.repository.save(task)
        self._notify("Task Archived", f"Task '{task.title}' has been archived")
        return task

    # ---------- search / filter ----------
    def search_tasks(self, status=None, priority=None, due_from=None,
                     due_to=None, title_contains=None):
        results = []
        for task in self.repository.find_all():
            if status is not None and task.status != status:
                continue
            if priority is not None and task.priority != priority:
                continue
            if due_from is not None and (task.due_date is None or task.due_date < due_from):
                continue
            if due_to is not None and (task.due_date is None or task.due_date > due_to):
                continue
            if title_contains is not None and title_contains.lower() not in task.title.lower():
                continue
            results.append(task)
        return results

    # ---------- overdue ----------
    def check_overdue_tasks(self):
        overdue = [t for t in self.repository.find_all() if t.is_overdue()]
        for task in overdue:
            self._notify("Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue