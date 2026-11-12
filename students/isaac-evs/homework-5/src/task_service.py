"""Business logic for TaskFlow: orchestrates the repository and the notification service."""

import logging
from datetime import datetime

from task import MAX_DESCRIPTION_LENGTH, Task, TaskPriority, TaskStatus, sort_by_priority

logger = logging.getLogger(__name__)

DEFAULT_RECIPIENT = "user@example.com"
DEFAULT_PHONE_NUMBER = "+15555550100"


class TaskService:
    """Creates, updates, archives and searches tasks, notifying the user of key events."""

    def __init__(
        self,
        repository,
        notification_service,
        clock=datetime.now,
        recipient=DEFAULT_RECIPIENT,
        phone_number=DEFAULT_PHONE_NUMBER,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.repository = repository
        self.notification_service = notification_service
        self.clock = clock
        self.recipient = recipient
        self.phone_number = phone_number

    def _notify_email(self, subject, body):
        """Send an email; a delivery failure is logged and never breaks the workflow."""
        try:
            self.notification_service.send_email(self.recipient, subject, body)
            return True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.warning("Email notification failed: %s", exc)
            return False

    def _notify_sms(self, message):
        """Send an SMS; a delivery failure is logged and never breaks the workflow."""
        try:
            self.notification_service.send_sms(self.phone_number, message)
            return True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.warning("SMS notification failed: %s", exc)
            return False

    def _get_existing(self, task_id):
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    def _ensure_title_available(self, title, current_task=None):
        existing = self.repository.find_by_title(title)
        if existing is None:
            return
        is_same_task = current_task is not None and (
            existing is current_task or (existing.id is not None and existing.id == current_task.id)
        )
        if not is_same_task:
            raise ValueError(f"Task with title '{title}' already exists")

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a task, enforcing unique titles, and notify the user."""
        task = Task(title, description, priority, due_date, now=self.clock())
        self._ensure_title_available(title)
        self.repository.save(task)
        self._notify_email("New Task Created", f"Task '{title}' has been created")
        return task

    def create_task_with_sms(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a task; URGENT tasks additionally trigger an SMS alert."""
        task = self.create_task(title, description, priority, due_date)
        if task.priority == TaskPriority.URGENT:
            self._notify_sms(f"URGENT task created: {task.title}")
        return task

    def get_task(self, task_id):
        """Return a task or raise ValueError if it does not exist."""
        return self._get_existing(task_id)

    def update_task(
        self, task_id, title=None, description=None, priority=None, due_date=None
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        """Update editable fields. All changes are validated before any is applied."""
        task = self._get_existing(task_id)
        if task.status == TaskStatus.ARCHIVED:
            raise ValueError("Archived tasks cannot be modified")

        now = self.clock()
        if title is not None:
            Task.validate_title(title)
            self._ensure_title_available(title, current_task=task)
        if priority is not None:
            Task.validate_priority(priority)
        if due_date is not None:
            Task.validate_due_date(due_date, now)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description[:MAX_DESCRIPTION_LENGTH]
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date
        task.touch(now)
        self.repository.save(task)
        return task

    def update_task_status(self, task_id, new_status):
        """Move a task along its lifecycle and notify the user of the change."""
        if not isinstance(new_status, TaskStatus):
            raise ValueError(f"Invalid status: {new_status!r}")
        task = self._get_existing(task_id)
        if not task.can_transition(new_status):
            raise ValueError(f"Invalid transition from {task.status.value} to {new_status.value}")

        old_status = task.status
        task.status = new_status
        task.touch(self.clock())
        self.repository.save(task)
        self._notify_email(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return task

    def delete_task(self, task_id):
        """Soft delete: archive the task. Archived tasks cannot be restored."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def purge_task(self, task_id):
        """Permanently delete an archived task. Only archived tasks may be purged."""
        task = self._get_existing(task_id)
        if task.status != TaskStatus.ARCHIVED:
            raise ValueError("Only archived tasks can be permanently deleted")
        return self.repository.delete(task_id)

    def check_overdue_tasks(self):
        """Find overdue tasks and notify the user about each one."""
        now = self.clock()
        overdue_tasks = [task for task in self.repository.find_all() if task.is_overdue(now)]
        for task in overdue_tasks:
            self._notify_email("Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue_tasks

    def search_tasks(
        self,
        status=None,
        priority=None,
        due_from=None,
        due_to=None,
        title_contains=None,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        """Search with any combination of filters; results are ordered by priority."""
        matches = self.repository.search(
            status=status,
            priority=priority,
            due_from=due_from,
            due_to=due_to,
            title_contains=title_contains,
        )
        return sort_by_priority(matches)
