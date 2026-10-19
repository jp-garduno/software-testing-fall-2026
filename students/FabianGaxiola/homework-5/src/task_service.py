"""Task management workflows and business rules."""

import logging
from datetime import datetime

from src.notification_service import NotificationError, NotificationService
from src.task import Task, TaskPriority, TaskStatus
from src.task_repository import DuplicateTaskError, TaskRepository

logger = logging.getLogger(__name__)
NOTIFICATION_RECIPIENT = "user@example.com"
URGENT_PHONE_NUMBER = "+10000000000"


class TaskNotFoundError(LookupError):
    """Raised when a requested task does not exist."""


class InvalidTaskTransitionError(ValueError):
    """Raised when a status change violates the task lifecycle."""


class TaskService:
    """Coordinate task validation, repository operations, and notifications."""

    def __init__(
        self, repository: TaskRepository, notification_service: NotificationService
    ) -> None:
        self.repository = repository
        self.notification_service = notification_service

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: datetime | None = None,
    ) -> Task:
        existing = self.repository.find_by_title(title)
        if existing is not None:
            raise DuplicateTaskError(f"Task with title '{title}' already exists")

        task = Task(title, description, priority, due_date)
        saved_task = self.repository.save(task)
        self._notify_email(
            "New Task Created",
            f"Task '{saved_task.title}' has been created",
        )
        if saved_task.priority == TaskPriority.URGENT:
            self._notify_sms(f"Urgent task '{saved_task.title}' has been created")
        return saved_task

    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self._get_task(task_id)
        if not task.can_transition(new_status):
            raise InvalidTaskTransitionError(
                f"Invalid transition from {task.status} to {new_status}"
            )

        old_status = task.status
        task.status = new_status
        task.updated_at = self._current_time(task)
        saved_task = self.repository.save(task)
        self._notify_email(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return saved_task

    def update_task(self, task_id: int, **changes: object) -> Task:
        task = self._get_task(task_id)
        if task.status == TaskStatus.ARCHIVED:
            raise InvalidTaskTransitionError("Archived tasks cannot be modified")
        if not changes:
            raise ValueError("At least one task field must be provided")

        allowed_fields = {"title", "description", "priority", "due_date"}
        unknown_fields = changes.keys() - allowed_fields
        if unknown_fields:
            raise ValueError(
                f"Unsupported task fields: {', '.join(sorted(unknown_fields))}"
            )

        title = changes.get("title", task.title)
        description = changes.get("description", task.description)
        priority = changes.get("priority", task.priority)
        due_date = changes.get("due_date", task.due_date)
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        Task.validate_title(title)
        Task.validate_description(description)
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority value")
        if due_date is not None:
            if not isinstance(due_date, datetime):
                raise ValueError("Due date must be a datetime")
            Task.validate_due_date(due_date)

        if "title" in changes:
            existing = self.repository.find_by_title(title)
            if existing is not None and existing.id != task.id:
                raise DuplicateTaskError(f"Task with title '{title}' already exists")

        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = due_date
        task.updated_at = self._current_time(task)
        return self.repository.save(task)

    def delete_task(self, task_id: int) -> Task:
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def search_tasks(  # pylint: disable=too-many-arguments
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        due_after: datetime | None = None,
        due_before: datetime | None = None,
        title: str | None = None,
    ) -> list[Task]:  # pylint: disable=too-many-arguments
        return self.repository.search(status, priority, due_after, due_before, title)

    def check_overdue_tasks(self, now: datetime | None = None) -> list[Task]:
        overdue_tasks = [
            task for task in self.repository.find_all() if task.is_overdue(now)
        ]
        for task in overdue_tasks:
            self._notify_email(
                "Task Overdue",
                f"Task '{task.title}' is overdue!",
            )
        return overdue_tasks

    def _get_task(self, task_id: int) -> Task:
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    @staticmethod
    def _current_time(task: Task) -> datetime:
        return datetime.now(task.created_at.tzinfo)

    def _notify_email(self, subject: str, body: str) -> None:
        try:
            self.notification_service.send_email(NOTIFICATION_RECIPIENT, subject, body)
        except NotificationError:
            logger.warning(
                "Unable to send email notification: %s", subject, exc_info=True
            )

    def _notify_sms(self, message: str) -> None:
        try:
            self.notification_service.send_sms(URGENT_PHONE_NUMBER, message)
        except NotificationError:
            logger.warning("Unable to send SMS notification", exc_info=True)
