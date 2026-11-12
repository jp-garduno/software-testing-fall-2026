"""Business logic layer for TaskFlow.

Orchestrates the repository and the notification service and enforces the
business rules (unique titles, valid transitions, archived tasks are frozen).
"""

import logging

from task import Task, TaskPriority, TaskStatus

logger = logging.getLogger(__name__)

DEFAULT_EMAIL = "user@example.com"
DEFAULT_PHONE = "+521234567890"

_UNSET = object()


class TaskService:
    """Create, update, archive, search and monitor tasks."""

    def __init__(self, repository, notification_service,
                 recipient_email=DEFAULT_EMAIL, recipient_phone=DEFAULT_PHONE):
        self.repository = repository
        self.notification_service = notification_service
        self.recipient_email = recipient_email
        self.recipient_phone = recipient_phone

    # ------------------------------------------------------------------ create
    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a task, enforcing a unique title, and notify the user."""
        if self.repository.find_by_title(title):
            raise ValueError(f"Task with title '{title}' already exists")

        task = Task(title, description, priority, due_date)
        self.repository.save(task)

        self._notify_email("New Task Created", f"Task '{title}' has been created")
        return task

    def create_task_with_sms(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a task; URGENT tasks additionally trigger an SMS."""
        task = self.create_task(title, description, priority, due_date)
        if priority == TaskPriority.URGENT:
            self._notify_sms(f"URGENT task created: {title}")
        return task

    # ------------------------------------------------------------------ read
    def get_task(self, task_id):
        return self._get_or_raise(task_id)

    def search_tasks(self, status=None, priority=None, due_from=None, due_to=None, title_contains=None):
        """Filter tasks; all provided filters are combined."""
        return self.repository.search(
            status=status,
            priority=priority,
            due_from=due_from,
            due_to=due_to,
            title_contains=title_contains,
        )

    # ------------------------------------------------------------------ update
    def update_task(self, task_id, title=_UNSET, description=_UNSET,
                    priority=_UNSET, due_date=_UNSET):
        """Update editable fields. Archived tasks cannot be modified."""
        task = self._get_or_raise(task_id)

        if task.status == TaskStatus.ARCHIVED:
            raise ValueError("Archived tasks cannot be modified")

        # Validate everything first so a failure never leaves a half-updated task.
        if title is not _UNSET:
            Task.validate_title(title)
            existing = self.repository.find_by_title(title)
            if existing and existing is not task:
                raise ValueError(f"Task with title '{title}' already exists")
        if due_date is not _UNSET and due_date is not None:
            Task.validate_due_date(due_date)

        if title is not _UNSET:
            task.title = title
        if description is not _UNSET:
            task.description = Task.normalize_description(description)
        if priority is not _UNSET:
            task.priority = priority
        if due_date is not _UNSET:
            task.due_date = due_date

        task.touch()
        self.repository.save(task)
        return task

    def update_task_status(self, task_id, new_status):
        """Move a task along a valid transition and notify the user."""
        task = self._get_or_raise(task_id)

        if not task.can_transition(new_status):
            raise ValueError(f"Invalid transition from {task.status.value} to {new_status.value}")

        old_status = task.status
        task.status = new_status
        task.touch()
        self.repository.save(task)

        self._notify_email(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return task

    # ------------------------------------------------------------------ delete
    def delete_task(self, task_id):
        """Soft delete: mark the task as ARCHIVED."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    # ------------------------------------------------------------------ overdue
    def check_overdue_tasks(self):
        """Notify about every overdue task and return them."""
        overdue = [task for task in self.repository.find_all() if task.is_overdue()]
        for task in overdue:
            self._notify_email("Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue

    # ------------------------------------------------------------------ helpers
    def _get_or_raise(self, task_id):
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    def _notify_email(self, subject, body):
        """Send an email; a notification failure must never break the workflow."""
        try:
            self.notification_service.send_email(self.recipient_email, subject, body)
        except Exception as exc:
            logger.warning("Email notification failed: %s", exc)

    def _notify_sms(self, message):
        try:
            self.notification_service.send_sms(self.recipient_phone, message)
        except Exception as exc:
            logger.warning("SMS notification failed: %s", exc)
