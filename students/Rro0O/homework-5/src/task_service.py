"""Business logic orchestrating the repository and notifications."""

# pylint: disable=import-error,too-many-arguments,too-many-positional-arguments

import logging

from task import Task, TaskPriority, TaskStatus

LOGGER = logging.getLogger(__name__)
DEFAULT_RECIPIENT = "user@example.com"
DEFAULT_PHONE = "+10000000000"
_UNSET = object()


class TaskService:
    """Create, update, search and archive tasks."""

    def __init__(self, repository, notification_service):
        """Init."""
        self.repository = repository
        self.notification_service = notification_service

    # -- helpers ---------------------------------------------------------
    def _notify_email(self, subject, body):
        """Send an email; failures are logged and never break the workflow."""
        try:
            self.notification_service.send_email(DEFAULT_RECIPIENT, subject, body)
        except Exception as error:  # pylint: disable=broad-exception-caught
            LOGGER.warning("Email notification failed: %s", error)

    def _notify_sms(self, message):
        """Send an SMS; failures are logged and never break the workflow."""
        try:
            self.notification_service.send_sms(DEFAULT_PHONE, message)
        except Exception as error:  # pylint: disable=broad-exception-caught
            LOGGER.warning("SMS notification failed: %s", error)

    def _get_task(self, task_id):
        """Get task."""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    def _ensure_unique_title(self, title, current=None):
        """Ensure unique title."""
        existing = self.repository.find_by_title(title)
        if existing and existing is not current:
            raise ValueError(f"Task with title '{title}' already exists")

    # -- creation --------------------------------------------------------
    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a task after validating uniqueness; notify by email."""
        self._ensure_unique_title(title)
        task = Task(title, description, priority, due_date)
        self.repository.save(task)
        self._notify_email("New Task Created", f"Task '{title}' has been created")
        return task

    def create_task_with_sms(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a task; URGENT tasks also trigger an SMS."""
        task = self.create_task(title, description, priority, due_date)
        if task.priority == TaskPriority.URGENT:
            self._notify_sms(f"URGENT task created: {title}")
        return task

    # -- updates ---------------------------------------------------------
    def update_task(self, task_id, title=None, description=None, priority=None, due_date=_UNSET):
        """Update editable fields of a non-archived task."""
        task = self._get_task(task_id)
        if task.status == TaskStatus.ARCHIVED:
            raise ValueError("Cannot modify an archived task")
        if title is not None:
            Task.validate_title(title)
            if title != task.title:
                self._ensure_unique_title(title, task)
            task.title = title
        if description is not None:
            task.description = description[:500]
        if priority is not None:
            task.priority = priority
        if due_date is not _UNSET and due_date is not None:
            Task.validate_due_date(due_date)
            task.due_date = due_date
        task.touch()
        self.repository.save(task)
        return task

    def update_task_status(self, task_id, new_status):
        """Move a task to ``new_status`` and notify."""
        task = self._get_task(task_id)
        if not task.can_transition(new_status):
            raise ValueError(f"Invalid transition from {task.status} to {new_status}")
        old_status = task.status
        task.status = new_status
        task.touch()
        self.repository.save(task)
        self._notify_email(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return task

    def delete_task(self, task_id):
        """Soft delete: mark the task as ARCHIVED."""
        return self.update_task_status(task_id, TaskStatus.ARCHIVED)

    # -- overdue ---------------------------------------------------------
    def check_overdue_tasks(self):
        """Notify about every overdue task and return them."""
        overdue = [task for task in self.repository.find_all() if task.is_overdue()]
        for task in overdue:
            self._notify_email("Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue

    # -- search ----------------------------------------------------------
    def search_tasks(
        self, status=None, priority=None, due_from=None, due_to=None, title_query=None
    ):
        """Filter tasks; all given filters are combined with AND."""
        results = []
        for task in self.repository.find_all():
            if status is not None and task.status != status:
                continue
            if priority is not None and task.priority != priority:
                continue
            if due_from is not None or due_to is not None:
                if task.due_date is None:
                    continue
                if due_from is not None and task.due_date < due_from:
                    continue
                if due_to is not None and task.due_date > due_to:
                    continue
            if title_query is not None and title_query.lower() not in task.title.lower():
                continue
            results.append(task)
        return results

    def sorted_by_priority(self):
        """Return all tasks, URGENT first."""
        return sorted(self.repository.find_all(), key=lambda t: t.priority.value, reverse=True)
