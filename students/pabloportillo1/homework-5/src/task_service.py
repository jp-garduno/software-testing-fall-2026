import logging

from notification_service import NotificationError, validate_email_address, validate_phone_number
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskFilter

logger = logging.getLogger(__name__)


class TaskNotFoundError(LookupError):
    """Raised when no task has the requested identifier."""


class DuplicateTitleError(ValueError):
    """Raised when another task already uses the requested title."""


class TaskService:
    """Enforces TaskFlow's business rules over a TaskRepository and notifies the task owner of changes.

    A failed notification is logged and never undoes or blocks the change that triggered it. URGENT
    tasks are also notified by SMS when the owner has a phone number.
    """

    def __init__(self, repository, notification_service, owner_email, owner_phone=None):
        self._repository = repository
        self._notifier = notification_service
        self._owner_email = validate_email_address(owner_email)
        self._owner_phone = None if owner_phone is None else validate_phone_number(owner_phone)

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Validate, store and announce a new task; raise DuplicateTitleError if the title is taken."""
        task = Task(title, description, priority, due_date)
        self._ensure_title_available(task.title)
        self._repository.save(task)
        self._notify(task, "New Task Created", f"Task '{task.title}' has been created")
        return task

    def get_task(self, task_id):
        """Return the task with the given identifier, or raise TaskNotFoundError."""
        task = self._repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def update_task(self, task_id, **changes):
        """Change title, description, priority and/or due_date; a new title must still be unique."""
        task = self.get_task(task_id)
        if changes.get("title") is not None:
            self._ensure_title_available(Task.validate_title(changes["title"]), renamed_task_id=task.task_id)
        task.update_details(**changes)
        self._repository.save(task)
        return task

    def update_task_status(self, task_id, new_status):
        """Move a task along its lifecycle, store it and notify the owner of the change."""
        task = self.get_task(task_id)
        old_status = task.status
        task.transition_to(new_status)
        self._repository.save(task)
        self._notify(
            task, "Task Status Updated", f"Task '{task.title}' changed from {old_status.value} to {new_status.value}"
        )
        return task

    def delete_task(self, task_id):
        """Soft delete: archive the task. Archived tasks cannot be restored."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def purge_task(self, task_id):
        """Permanently delete a task; it cannot be recovered afterwards."""
        if not self._repository.delete(task_id):
            raise TaskNotFoundError(f"Task {task_id} not found")

    def check_overdue_tasks(self):
        """Notify the owner about every overdue task and return those tasks."""
        overdue_tasks = [task for task in self._repository.find_all() if task.is_overdue()]
        for task in overdue_tasks:
            self._notify(task, "Task Overdue", f"Task '{task.title}' is overdue (due {task.due_date:%Y-%m-%d %H:%M})")
        return overdue_tasks

    def search_tasks(self, task_filter=None):
        """Return the tasks matching task_filter (all tasks when omitted), highest priority first."""
        return self._repository.search(task_filter or TaskFilter())

    def _ensure_title_available(self, title, renamed_task_id=None):
        existing = self._repository.find_by_title(title)
        if existing is not None and (renamed_task_id is None or existing.task_id != renamed_task_id):
            raise DuplicateTitleError(f"Task with title '{title}' already exists")

    def _notify(self, task, subject, body):
        self._send_safely(self._notifier.send_email, self._owner_email, subject, body)
        if task.priority is TaskPriority.URGENT and self._owner_phone is not None:
            self._send_safely(self._notifier.send_sms, self._owner_phone, f"{subject}: {body}")

    @staticmethod
    def _send_safely(send, *args):
        try:
            send(*args)
        except NotificationError as error:
            logger.warning("Notification not delivered: %s", error)
