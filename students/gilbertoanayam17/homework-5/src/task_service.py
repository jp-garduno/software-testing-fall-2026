"""Business logic for TaskFlow: enforces the rules and orchestrates repository and notifications."""

import logging

from notification_service import NotificationError
from task import Task, TaskPriority, TaskStateError, TaskStatus
from task_repository import TaskFilter

logger = logging.getLogger(__name__)


class TaskNotFoundError(LookupError):
    """Raised when no task exists with the requested id."""


class DuplicateTitleError(ValueError):
    """Raised when another task already uses the requested title."""


class TaskService:
    """Use cases of TaskFlow. Repository failures propagate; notification failures never do."""

    def __init__(self, repository, notification_service, recipient_email="user@example.com", recipient_phone=None):
        self.repository = repository
        self.notification_service = notification_service
        self.recipient_email = recipient_email
        self.recipient_phone = recipient_phone

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Validate, check the title is unique, save, then notify."""
        task = Task(title, description, priority, due_date)
        self._ensure_title_available(task.title)
        self.repository.save(task)
        self._notify(task, "New Task Created", f"Task '{task.title}' has been created")
        return task

    def get_task(self, task_id):
        """Return the task with that id or raise TaskNotFoundError."""
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def update_task(self, task_id, **changes):
        """Update title, description, priority and/or due_date; a new title must stay unique."""
        task = self.get_task(task_id)
        if changes.get("title") is not None:
            self._ensure_title_available(changes["title"], allowed_id=task.id)
        task.update(**changes)
        self.repository.save(task)
        return task

    def update_task_status(self, task_id, new_status):
        """Apply a lifecycle transition, save it and notify the change."""
        task = self.get_task(task_id)
        old_status = task.transition_to(new_status)
        self.repository.save(task)
        self._notify(
            task, "Task Status Updated", f"Task '{task.title}' changed from {old_status.value} to {new_status.value}"
        )
        return task

    def delete_task(self, task_id):
        """Soft delete: archive the task. Archived tasks cannot be restored."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def purge_task(self, task_id):
        """Permanently delete an archived task. This cannot be undone."""
        task = self.get_task(task_id)
        if task.status is not TaskStatus.ARCHIVED:
            raise TaskStateError("Only archived tasks can be permanently deleted")
        self.repository.delete(task_id)

    def search_tasks(self, **criteria):
        """Filter by status, priority, due date range and/or partial title (see TaskFilter)."""
        return self.repository.search(TaskFilter(**criteria))

    def list_by_priority(self):
        """All tasks ordered URGENT > HIGH > MEDIUM > LOW, oldest first within the same priority."""
        return sorted(self.repository.find_all(), key=lambda task: (-task.priority.value, task.created_at))

    def check_overdue_tasks(self):
        """Notify every overdue task and return them. Meant to be called periodically by a scheduler."""
        overdue = [task for task in self.repository.find_all() if task.is_overdue()]
        for task in overdue:
            self._notify(task, "Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue

    def _ensure_title_available(self, title, allowed_id=None):
        existing = self.repository.find_by_title(title)
        if existing is not None and existing.id != allowed_id:
            raise DuplicateTitleError(f"Task with title '{title.strip()}' already exists")

    def _notify(self, task, subject, body):
        """Email always; URGENT tasks also escalate to SMS when a phone number is configured."""
        self._deliver(self.notification_service.send_email, self.recipient_email, subject, body)
        if task.priority is TaskPriority.URGENT and self.recipient_phone:
            self._deliver(self.notification_service.send_sms, self.recipient_phone, f"{subject}: {body}")

    @staticmethod
    def _deliver(send, *args):
        try:
            send(*args)
        except NotificationError as error:
            # Best effort: the task operation already succeeded and must not be undone by a delivery problem.
            logger.warning("Notification could not be delivered: %s", error)
