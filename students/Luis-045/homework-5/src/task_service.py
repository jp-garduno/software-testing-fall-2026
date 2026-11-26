"""Task workflows orchestrating the real model and external dependency contracts."""

import logging
from collections.abc import Callable
from copy import copy
from datetime import datetime

from .notification_service import NotificationError, NotificationService
from .task import Task, TaskPriority, TaskStatus, as_utc, utc_now
from .task_repository import TaskRepository

LOGGER = logging.getLogger(__name__)


class TaskService:
    """Manage tasks with injected persistence, notifications and time."""

    def __init__(
        self,
        repository: TaskRepository,
        notification_service: NotificationService,
        *,
        clock: Callable[[], datetime] = utc_now,
        phone_number: str | None = None,
    ) -> None:
        self.repository = repository
        self.notification_service = notification_service
        self.clock = clock
        self.phone_number = phone_number

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.LOW,
        due_date: datetime | None = None,
    ) -> Task:
        """Validate, persist and notify creation of a task with a unique title."""
        task = Task(title, description, priority, due_date, clock=self.clock)
        if self.repository.find_by_title(task.title) is not None:
            raise ValueError(f"Task with title '{task.title}' already exists")
        self.repository.save(task)
        self._notify(task, "New Task Created", f"Task '{task.title}' has been created")
        return task

    def update_task_status(self, task_id: str, new_status: TaskStatus) -> Task:
        """Apply a lifecycle transition through the same validated update workflow."""
        return self.update_task(task_id, status=new_status)

    def update_task(self, task_id: str, **changes) -> Task:
        """Validate all proposed changes before saving a detached snapshot."""
        original = self._find_task(task_id)
        if original.status is TaskStatus.ARCHIVED:
            raise ValueError("Archived tasks cannot be modified")
        unknown = set(changes) - {
            "title",
            "description",
            "priority",
            "due_date",
            "status",
        }
        if unknown:
            raise ValueError(f"Unknown fields: {', '.join(sorted(unknown))}")
        if not changes:
            return copy(original)
        if changes.get("status") is TaskStatus.ARCHIVED and len(changes) > 1:
            raise ValueError("Cannot modify other fields when archiving")
        new_status = changes.get("status", original.status)
        if "status" in changes and not original.can_transition(new_status):
            raise ValueError(
                f"Invalid transition from {original.status} to {new_status}"
            )
        updated = self._apply_fields(original, changes)
        updated.status = new_status
        self.repository.save(updated)
        if "status" in changes:
            self._notify(
                updated,
                "Task Status Updated",
                f"Task '{updated.title}' changed from {original.status.value} to {new_status.value}",
            )
        else:
            self._notify(
                updated, "Task Updated", f"Task '{updated.title}' has been updated"
            )
        return updated

    def delete_task(self, task_id: str) -> Task:
        """Soft delete by archiving, preserving the stored task and its identity."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    # Each keyword is an independent filter required by the assignment.
    def search_tasks(  # pylint: disable=too-many-arguments
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        title: str | None = None,
    ) -> list[Task]:
        """Combine optional filters; due-date bounds are inclusive and title ignores case."""
        if status is not None and not isinstance(status, TaskStatus):
            raise ValueError("Status must be a TaskStatus")
        if priority is not None:
            Task.validate_priority(priority)
        if title is not None and not isinstance(title, str):
            raise ValueError("Title filter must be a string")
        start = as_utc(start_date) if start_date is not None else None
        end = as_utc(end_date) if end_date is not None else None
        if start is not None and end is not None and start > end:
            raise ValueError("Invalid date range: start is later than end")
        return [
            task
            for task in self.repository.find_all()
            if (status is None or task.status is status)
            and (priority is None or task.priority is priority)
            and (title is None or title.casefold() in task.title.casefold())
            and (
                start is None or (task.due_date is not None and task.due_date >= start)
            )
            and (end is None or (task.due_date is not None and task.due_date <= end))
        ]

    def check_overdue_tasks(self) -> list[Task]:
        """Find overdue tasks on demand and notify through configured channels."""
        current = as_utc(self.clock())
        overdue_tasks = [
            task for task in self.repository.find_all() if task.is_overdue(now=current)
        ]
        for task in overdue_tasks:
            self._notify(task, "Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue_tasks

    def _find_task(self, task_id: str) -> Task:
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")
        return task

    def _apply_fields(self, original: Task, changes: dict) -> Task:
        updated = copy(original)
        current = as_utc(self.clock())
        if "title" in changes:
            Task.validate_title(changes["title"])
            if changes["title"] != original.title:
                existing = self.repository.find_by_title(changes["title"])
                if existing is not None and existing.id != original.id:
                    raise ValueError(
                        f"Task with title '{changes['title']}' already exists"
                    )
            updated.title = changes["title"]
        if "description" in changes:
            updated.description = Task.validate_description(changes["description"])
        if "priority" in changes:
            Task.validate_priority(changes["priority"])
            updated.priority = changes["priority"]
        if "due_date" in changes:
            due_date = changes["due_date"]
            updated.due_date = (
                None
                if due_date is None
                else updated.validate_due_date(due_date, now=current)
            )
        updated.clock = self.clock
        updated.updated_at = current
        return updated

    def _notify(self, task: Task, subject: str, body: str) -> None:
        # Delivery errors are isolated from an already committed business operation.
        try:
            self.notification_service.send_email("user@example.com", subject, body)
        except NotificationError as error:
            LOGGER.warning("Email notification failed for %s: %s", task.id, error)
        if task.priority is TaskPriority.URGENT and self.phone_number:
            try:
                self.notification_service.send_sms(self.phone_number, body)
            except NotificationError as error:
                LOGGER.warning("SMS notification failed for %s: %s", task.id, error)
