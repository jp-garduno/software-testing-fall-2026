"""Task operations. Persist first; notification outages never undo a saved task."""

from copy import copy
from datetime import datetime
import logging

from task import Task, TaskPriority, TaskStatus

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repository, notification_service, clock=datetime.now,
                 recipient="user@example.com", phone_number="+15555550100"):
        self.repository = repository
        self.notification_service = notification_service
        self.clock = clock
        self.recipient = recipient
        self.phone_number = phone_number

    def _notify(self, subject, body, sms=False):
        try:
            self.notification_service.send_email(self.recipient, subject, body)
        except Exception:
            logger.warning("Email notification failed", exc_info=True)
        if sms:
            try:
                self.notification_service.send_sms(self.phone_number, body)
            except Exception:
                logger.warning("SMS notification failed", exc_info=True)

    def _get_task(self, task_id):
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")
        return task

    def _ensure_unique(self, title, task_id=None):
        existing = self.repository.find_by_title(title)
        if existing is not None and existing.id != task_id:
            raise ValueError(f"Task with title '{title}' already exists")

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        task = Task(title, description, priority, due_date, clock=self.clock)
        self._ensure_unique(title)
        self.repository.save(task)
        self._notify("New Task Created", f"Task '{title}' has been created")
        return task

    def create_task_with_sms(self, title, description="", priority=TaskPriority.LOW,
                             due_date=None):
        task = self.create_task(title, description, priority, due_date)
        if priority == TaskPriority.URGENT:
            try:
                self.notification_service.send_sms(
                    self.phone_number, f"Urgent task '{title}' has been created")
            except Exception:
                logger.warning("SMS notification failed", exc_info=True)
        return task

    def update_task(self, task_id, **changes):
        original = self._get_task(task_id)
        if original.status == TaskStatus.ARCHIVED:
            raise ValueError("Archived tasks cannot be modified")
        if not changes or changes.keys() - {"title", "description", "priority", "due_date"}:
            raise ValueError("Supply only title, description, priority or due_date")
        # Validate a copy so invalid edits or failed saves cannot mutate stored state.
        updated = copy(original)
        for name, value in changes.items():
            setattr(updated, name, value)
        updated.validate_title(updated.title)
        updated.validate_description(updated.description)
        updated.validate_priority(updated.priority)
        if "due_date" in changes:
            updated.validate_due_date(updated.due_date)
        self._ensure_unique(updated.title, updated.id)
        updated.updated_at = self.clock()
        self.repository.save(updated)
        return updated

    def update_task_status(self, task_id, new_status):
        original = self._get_task(task_id)
        if not original.can_transition(new_status):
            raise ValueError(f"Invalid transition from {original.status} to {new_status}")
        updated = copy(original)
        updated.status = new_status
        updated.updated_at = self.clock()
        self.repository.save(updated)
        self._notify("Task Status Updated",
                     f"Task '{updated.title}' changed from {original.status.value} "
                     f"to {new_status.value}")
        return updated

    def delete_task(self, task_id):
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    def permanently_delete_task(self, task_id):
        self._get_task(task_id)
        self.repository.delete(task_id)

    def check_overdue_tasks(self):
        overdue = [task for task in self.repository.find_all() if task.is_overdue()]
        for task in overdue:
            self._notify("Task Overdue", f"Task '{task.title}' is overdue",
                         sms=task.priority == TaskPriority.URGENT)
        return overdue

    def search_tasks(self, status=None, priority=None, start_date=None,
                     end_date=None, title=None):
        if status is not None and not isinstance(status, TaskStatus):
            raise ValueError("Status must be a TaskStatus")
        if priority is not None:
            Task.validate_priority(priority)
        if start_date is not None and end_date is not None and start_date > end_date:
            raise ValueError("Date range is reversed")
        result = []
        for task in self.repository.find_all():
            if status is not None and task.status != status:
                continue
            if priority is not None and task.priority != priority:
                continue
            if title is not None and title.casefold() not in task.title.casefold():
                continue
            if start_date is not None and (task.due_date is None or task.due_date < start_date):
                continue
            if end_date is not None and (task.due_date is None or task.due_date > end_date):
                continue
            result.append(task)
        return sorted(result, key=lambda task: task.priority, reverse=True)
