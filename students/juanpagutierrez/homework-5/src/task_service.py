"""Business logic layer: orchestrates the repository and the notification service."""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from notification_service import NotificationError
from task import Task, TaskPriority, TaskStatus
from task_repository import RepositoryError, TaskQuery

logger = logging.getLogger(__name__)

UPDATABLE_FIELDS = ("title", "description", "priority", "due_date")


class TaskServiceError(Exception):
    """Base class for errors raised by TaskService."""


class TaskNotFoundError(TaskServiceError, LookupError):
    """Raised when no task has the requested id."""


class DuplicateTitleError(TaskServiceError, ValueError):
    """Raised when another task already uses the title."""


class ArchivedTaskError(TaskServiceError, ValueError):
    """Raised when an archived task would be modified."""


class ServiceUnavailableError(TaskServiceError):
    """Raised when the repository fails."""


@dataclass(frozen=True)
class Recipient:
    """Who receives notifications. SMS is only sent when a phone is set."""

    email: str = "user@example.com"
    phone: Optional[str] = None


class TaskService:

    def __init__(self, repository, notification_service, recipient=None, clock=None):
        self.repository = repository
        self.notification_service = notification_service
        self.recipient = recipient or Recipient()
        self.clock = clock or datetime.now
        self.failed_notifications = []

    # -- helpers -------------------------------------------------------------

    def _repo(self, operation, *args):
        """Call a repository method, translating storage failures."""
        try:
            return getattr(self.repository, operation)(*args)
        except RepositoryError as error:
            raise ServiceUnavailableError(f"Task storage unavailable: {error}") from error

    def _notify(self, subject, body, urgent=False):
        """Send an email, plus an SMS when urgent. Delivery failures never break the workflow."""
        channels = [("email", lambda: self.notification_service.send_email(self.recipient.email, subject, body))]
        if urgent and self.recipient.phone:
            channels.append(("sms", lambda: self.notification_service.send_sms(self.recipient.phone, body)))

        for channel, send in channels:
            try:
                send()
            except NotificationError as error:
                logger.warning("%s notification '%s' failed: %s", channel, subject, error)
                self.failed_notifications.append((channel, subject, str(error)))

    def _ensure_title_available(self, title, task_id=None):
        existing = self._repo("find_by_title", title)
        if existing is not None and existing.id != task_id:
            raise DuplicateTitleError(f"Task with title '{title}' already exists")

    # -- commands ------------------------------------------------------------

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        self._ensure_title_available(title)
        task = Task(title, description, priority, due_date, now=self.clock())
        self._repo("save", task)
        self._notify(
            "New Task Created",
            f"Task '{title}' has been created",
            urgent=priority == TaskPriority.URGENT,
        )
        return task

    def get_task(self, task_id):
        task = self._repo("find_by_id", task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def update_task(self, task_id, **changes):
        """Update title, description, priority and/or due_date of a non-archived task."""
        unknown = sorted(set(changes) - set(UPDATABLE_FIELDS))
        if unknown:
            raise ValueError(f"Cannot update field(s): {', '.join(unknown)}")

        task = self.get_task(task_id)
        if task.is_archived:
            raise ArchivedTaskError(f"Task {task_id} is archived and cannot be modified")

        now = self.clock()
        if "title" in changes:
            Task.validate_title(changes["title"])
            self._ensure_title_available(changes["title"], task_id=task.id)
        if "description" in changes:
            Task.validate_description(changes["description"])
            changes["description"] = changes["description"] or ""
        if changes.get("due_date") is not None:
            Task.validate_due_date(changes["due_date"], now)

        for field, value in changes.items():
            setattr(task, field, value)
        task.touch(now)
        self._repo("save", task)
        return task

    def update_task_status(self, task_id, new_status):
        task = self.get_task(task_id)
        old_status = task.transition_to(new_status, now=self.clock())
        self._repo("save", task)
        self._notify(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
            urgent=task.priority == TaskPriority.URGENT,
        )
        return task

    def delete_task(self, task_id):
        """Soft delete: the task is archived and stays in the repository."""
        task = self.get_task(task_id)
        if task.is_archived:
            raise ArchivedTaskError(f"Task {task_id} is already archived")
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def purge_task(self, task_id):
        """Permanently delete an archived task. This cannot be undone."""
        task = self.get_task(task_id)
        if not task.is_archived:
            raise ValueError(f"Task {task_id} must be archived before it can be purged")
        return self._repo("delete", task_id)

    # -- queries -------------------------------------------------------------

    def check_overdue_tasks(self):
        """Notify about every overdue task and return them."""
        now = self.clock()
        overdue = [task for task in self._repo("find_all") if task.is_overdue(now)]
        for task in overdue:
            self._notify(
                "Task Overdue",
                f"Task '{task.title}' is overdue!",
                urgent=task.priority in (TaskPriority.HIGH, TaskPriority.URGENT),
            )
        return overdue

    def search_tasks(self, **criteria):
        """Search by status, priority, due_after, due_before and/or title_contains."""
        return self._repo("search", TaskQuery(**criteria))

    def list_active_tasks_by_priority(self):
        """Non-archived tasks, most urgent first."""
        return sorted(task for task in self._repo("find_all") if not task.is_archived)
