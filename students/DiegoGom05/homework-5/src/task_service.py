import logging

from task import Task, TaskPriority

logger = logging.getLogger(__name__)

DEFAULT_EMAIL = "user@example.com"
DEFAULT_PHONE = "+521234567890"


class TaskService:
    """Lógica de negocio. Orquesta TaskRepository y NotificationService."""

    def __init__(self, repository, notification_service):
        self.repository = repository
        self.notification_service = notification_service

    # ---------- Notificaciones (nunca rompen el flujo) ----------
    def _notify_email(self, subject, body):
        try:
            self.notification_service.send_email(DEFAULT_EMAIL, subject, body)
            return True
        except Exception as exc:
            logger.warning("Email notification failed: %s", exc)
            return False

    def _notify_sms(self, message):
        try:
            self.notification_service.send_sms(DEFAULT_PHONE, message)
            return True
        except Exception as exc:
            logger.warning("SMS notification failed: %s", exc)
            return False

    def _get_task_or_fail(self, task_id):
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    # ---------- Creación ----------
    def create_task(
        self, title, description="", priority=TaskPriority.LOW, due_date=None
    ):
        if self.repository.find_by_title(title):
            raise ValueError(f"Task with title '{title}' already exists")

        task = Task(title, description, priority, due_date)
        self.repository.save(task)
        self._notify_email("New Task Created", f"Task '{title}' has been created")
        return task

    def create_task_with_sms(
        self, title, description="", priority=TaskPriority.LOW, due_date=None
    ):
        """Igual que create_task, pero las tareas URGENT también envían SMS."""
        task = self.create_task(title, description, priority, due_date)
        if priority == TaskPriority.URGENT:
            self._notify_sms(f"URGENT task created: '{title}'")
        return task

    # ---------- Lectura ----------
    def get_task(self, task_id):
        return self._get_task_or_fail(task_id)

    # ---------- Actualización ----------
    def update_task(
        self, task_id, title=None, description=None, priority=None, due_date=None
    ):
        task = self._get_task_or_fail(task_id)

        if title is not None and title != task.title:
            existing = self.repository.find_by_title(title)
            if existing and existing.id != task.id:
                raise ValueError(f"Task with title '{title}' already exists")

        task.update(title, description, priority, due_date)
        self.repository.save(task)
        return task

    def update_task_status(self, task_id, new_status):
        task = self._get_task_or_fail(task_id)

        old_status = task.status
        task.change_status(new_status)  # lanza ValueError si la transición es inválida
        self.repository.save(task)

        self._notify_email(
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {new_status.value}",
        )
        return task

    # ---------- Eliminación (soft delete) ----------
    def delete_task(self, task_id):
        task = self._get_task_or_fail(task_id)
        task.archive()
        self.repository.save(task)
        return task

    # ---------- Vencimiento ----------
    def check_overdue_tasks(self):
        overdue = [t for t in self.repository.find_all() if t.is_overdue()]
        for task in overdue:
            self._notify_email("Task Overdue", f"Task '{task.title}' is overdue!")
        return overdue

    # ---------- Búsqueda y filtros ----------
    def search_tasks(
        self, status=None, priority=None, due_from=None, due_to=None, title=None
    ):
        results = self.repository.find_all()

        if status is not None:
            results = [t for t in results if t.status == status]
        if priority is not None:
            results = [t for t in results if t.priority == priority]
        if due_from is not None:
            results = [t for t in results if t.due_date and t.due_date >= due_from]
        if due_to is not None:
            results = [t for t in results if t.due_date and t.due_date <= due_to]
        if title:
            results = [t for t in results if title.lower() in t.title.lower()]

        return results
