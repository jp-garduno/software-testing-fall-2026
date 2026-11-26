"""Business logic layer: orchestrates the Task model, the repository and notifications."""

import logging
from datetime import datetime

from errors import ArchivedTaskError, DuplicateTaskError, TaskNotFoundError
from task import Task, TaskPriority, TaskStatus

logger = logging.getLogger(__name__)

DEFAULT_RECIPIENT = "user@example.com"


class TaskService:
    """Use cases of TaskFlow.

    Repository errors propagate (the operation failed and nothing was notified).
    Notification errors never break a workflow: they are logged and ignored,
    because the task change was already persisted.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        repository,
        notification_service,
        clock=datetime.now,
        recipient=DEFAULT_RECIPIENT,
        phone_number=None,
    ):
        self.repository = repository
        self.notification_service = notification_service
        self.clock = clock
        self.recipient = recipient
        self.phone_number = phone_number

    # --------------------------------------------------------------- creation
    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        if self.repository.find_by_title(title):
            raise DuplicateTaskError(f"Task with title '{title}' already exists")

        task = Task(title, description, priority, due_date, now=self.clock())
        self.repository.save(task)

        self._notify_email("New Task Created", f"Task '{task.title}' has been created")
        if task.priority == TaskPriority.URGENT:
            self._notify_sms(f"URGENT task created: {task.title}")
        return task

    # ---------------------------------------------------------------- queries
    def get_task(self, task_id):
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def search_tasks(self, **filters):
        """Filter tasks (see TaskRepository.search) and sort them by priority."""
        return sorted(self.repository.search(**filters), key=Task.sort_key)

    def list_by_priority(self):
        return sorted(self.repository.find_all(), key=Task.sort_key)

    # ---------------------------------------------------------------- updates
    def update_task(self, task_id, **changes):
        """Update title/description/priority/due_date; the title must stay unique."""
        task = self.get_task(task_id)
        if "title" in changes:
            other = self.repository.find_by_title(changes["title"])
            if other is not None and other.task_id != task.task_id:
                raise DuplicateTaskError(f"Task with title '{changes['title']}' already exists")
        task.update(now=self.clock(), **changes)
        self.repository.save(task)
        return task

    def update_task_status(self, task_id, new_status):
        task = self.get_task(task_id)
        old_status = task.transition_to(new_status, now=self.clock())
        self.repository.save(task)
        self._notify_email(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return task

    # ---------------------------------------------------------------- removal
    def delete_task(self, task_id):
        """Soft delete: the task is archived and can never be restored."""
        task = self.get_task(task_id)
        if task.status == TaskStatus.ARCHIVED:
            raise ArchivedTaskError(f"Task {task_id} is already archived")
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def purge_task(self, task_id):
        """Permanent delete: the task cannot be recovered afterwards."""
        if not self.repository.delete(task_id):
            raise TaskNotFoundError(f"Task {task_id} not found")

    # ---------------------------------------------------------------- overdue
    def check_overdue_tasks(self):
        """Find overdue tasks and send one notification per task."""
        now = self.clock()
        overdue = [task for task in self.repository.find_all() if task.is_overdue(now)]
        for task in overdue:
            self._notify_email("Task Overdue", f"Task '{task.title}' is overdue!")
            if task.priority == TaskPriority.URGENT:
                self._notify_sms(f"URGENT task overdue: {task.title}")
        return overdue

    # ---------------------------------------------------------- notifications
    def _notify_email(self, subject, body):
        try:
            self.notification_service.send_email(self.recipient, subject, body)
            return True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.warning("Email notification failed: %s", exc)
            return False

    def _notify_sms(self, message):
        if not self.phone_number:
            return False
        try:
            self.notification_service.send_sms(self.phone_number, message)
            return True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.warning("SMS notification failed: %s", exc)
            return False
