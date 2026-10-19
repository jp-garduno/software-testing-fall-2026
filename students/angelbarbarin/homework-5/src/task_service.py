"""Business logic for TaskFlow.

TaskService enforces the business rules and orchestrates the repository (persistence)
and the notification service (external messaging):

* Repository failures propagate: if a task cannot be saved, nothing is notified.
* Notification failures never break a workflow: they are logged and counted in
  ``failed_notifications`` so the task operation itself still succeeds.
"""

from __future__ import annotations

import logging
from datetime import datetime

from task import InvalidTransitionError, Task, TaskPriority, TaskStatus

logger = logging.getLogger(__name__)

DEFAULT_RECIPIENT = "user@example.com"


class TaskNotFoundError(LookupError):
    """Raised when a task id does not exist."""


class DuplicateTaskError(ValueError):
    """Raised when a title is already used by another task."""


class TaskService:
    """Creates, updates, archives and queries tasks."""

    def __init__(
        self,
        repository,
        notification_service,
        recipient: str = DEFAULT_RECIPIENT,
        sms_number: str | None = None,
    ) -> None:
        self.repository = repository
        self.notification_service = notification_service
        self.recipient = recipient
        self.sms_number = sms_number
        self.failed_notifications = 0

    # ------------------------------------------------------------------ #
    # Create
    # ------------------------------------------------------------------ #
    def create_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: datetime | None = None,
    ) -> Task:
        """Validate, check the title is unique, save and notify."""
        task = Task(title, description, priority, due_date)
        self._ensure_unique_title(title)
        self.repository.save(task)

        self._notify(self.notification_service.notify_task_created, self.recipient, task)
        if task.priority == TaskPriority.URGENT and self.sms_number:
            self._notify(self.notification_service.notify_urgent_sms, self.sms_number, task)
        return task

    # ------------------------------------------------------------------ #
    # Read
    # ------------------------------------------------------------------ #
    def get_task(self, task_id: str) -> Task:
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def search_tasks(self, **filters) -> list[Task]:
        """Delegate to the repository search (status, priority, due range, title)."""
        return self.repository.search(**filters)

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #
    def update_task(self, task_id: str, **fields) -> Task:
        """Update title, description, priority and/or due_date.

        Unknown field names are rejected, a new title must stay unique, and archived
        tasks cannot be modified. Saves only when something actually changed.
        """
        allowed = {"title", "description", "priority", "due_date"}
        unknown = set(fields) - allowed
        if unknown:
            raise ValueError(f"Cannot update field(s): {', '.join(sorted(unknown))}")

        task = self.get_task(task_id)
        if task.is_archived:
            raise InvalidTransitionError("Archived tasks cannot be modified")

        new_title = fields.get("title")
        if new_title is not None and new_title.strip().casefold() != task.title.strip().casefold():
            self._ensure_unique_title(new_title, exclude_id=task.id)

        if task.update_fields(**fields):
            self.repository.save(task)
        return task

    def update_task_status(self, task_id: str, new_status: TaskStatus) -> Task:
        """Move a task to a new status, save it and notify the change."""
        task = self.get_task(task_id)
        old_status = task.transition_to(new_status)
        self.repository.save(task)
        self._notify(self.notification_service.notify_status_change, self.recipient, task, old_status)
        return task

    # ------------------------------------------------------------------ #
    # Delete
    # ------------------------------------------------------------------ #
    def delete_task(self, task_id: str) -> Task:
        """Soft delete: archive the task. Archived tasks cannot be restored."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def purge_task(self, task_id: str) -> None:
        """Permanently delete a task. Only archived tasks can be purged."""
        task = self.get_task(task_id)
        if not task.is_archived:
            raise InvalidTransitionError("Only archived tasks can be permanently deleted")
        if not self.repository.delete(task_id):
            raise TaskNotFoundError(f"Task {task_id} not found")

    # ------------------------------------------------------------------ #
    # Overdue
    # ------------------------------------------------------------------ #
    def check_overdue_tasks(self, now: datetime | None = None) -> list[Task]:
        """Find overdue tasks and send one notification per task."""
        current = now or datetime.now()
        overdue = [task for task in self.repository.find_all() if task.is_overdue(current)]
        for task in overdue:
            self._notify(self.notification_service.notify_overdue, self.recipient, task)
        return overdue

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _ensure_unique_title(self, title: str, exclude_id: str | None = None) -> None:
        existing = self.repository.find_by_title(title)
        if existing is not None and existing.id != exclude_id:
            raise DuplicateTaskError(f"Task with title '{title}' already exists")

    def _notify(self, send, *args) -> bool:
        """Call a notification method; log and count failures instead of raising."""
        try:
            send(*args)
            return True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.failed_notifications += 1
            logger.warning("Notification failed: %s", exc)
            return False
