"""Application service coordinating tasks, persistence, and notifications."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from .notification_service import NotificationService
from .task import Task, TaskPriority, TaskStatus
from .task_repository import TaskRepository


class TaskService:
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
        if self.repository.find_by_title(title):
            raise ValueError(f"Task with title '{title}' already exists")
        task = Task(title, description, priority, due_date)
        self.repository.save(task)
        self._notify_creation(task)
        return task

    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self._get_task(task_id)
        old_status = task.status
        task.transition_to(new_status)
        self.repository.save(task)
        self._notify_status_change(task, old_status)
        return task

    def update_task(
        self,
        task_id: int,
        *,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        due_date: datetime | None = None,
    ) -> Task:
        task = self._get_task(task_id)
        if title is not None:
            existing = self.repository.find_by_title(title)
            if existing is not None and existing.id != task.id:
                raise ValueError(f"Task with title '{title}' already exists")
        task.update_details(
            title=title, description=description, priority=priority, due_date=due_date
        )
        self.repository.save(task)
        return task

    def archive_task(self, task_id: int) -> Task:
        task = self._get_task(task_id)
        if task.status is not TaskStatus.ARCHIVED:
            return self.update_task_status(task_id, TaskStatus.ARCHIVED)
        return task

    def check_overdue_tasks(self, now: datetime | None = None) -> list[Task]:
        overdue_tasks = [
            task for task in self.repository.find_all() if task.is_overdue(now)
        ]
        for task in overdue_tasks:
            self._send_safely(
                "send_email",
                "user@example.com",
                "Task Overdue",
                f"Task '{task.title}' is overdue.",
            )
        return overdue_tasks

    def search_tasks(
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        title_contains: str | None = None,
        due_between: tuple[datetime, datetime] | None = None,
    ) -> list[Task]:
        results: Iterable[Task] = self.repository.find_all()
        if status is not None:
            results = (task for task in results if task.status is status)
        if priority is not None:
            results = (task for task in results if task.priority is priority)
        if title_contains is not None:
            needle = title_contains.lower()
            results = (task for task in results if needle in task.title.lower())
        if due_between is not None:
            start, end = due_between
            results = (
                task
                for task in results
                if task.due_date is not None and start <= task.due_date <= end
            )
        return list(results)

    def _get_task(self, task_id: int) -> Task:
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")
        return task

    def _notify_creation(self, task: Task) -> None:
        self._send_safely(
            "send_email",
            "user@example.com",
            "New Task Created",
            f"Task '{task.title}' has been created.",
        )
        if task.priority is TaskPriority.URGENT:
            self._send_safely("send_sms", "+15555550100", f"Urgent task: {task.title}")

    def _notify_status_change(self, task: Task, old_status: TaskStatus) -> None:
        self._send_safely(
            "send_email",
            "user@example.com",
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {task.status.value}.",
        )

    def _send_safely(self, method_name: str, *args: str) -> None:
        """Notifications are best effort and never roll back persisted work."""
        try:
            getattr(self.notification_service, method_name)(*args)
        except Exception:  # pylint: disable=broad-exception-caught
            pass
