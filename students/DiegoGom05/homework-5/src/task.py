import uuid
from datetime import datetime
from enum import Enum

MAX_DESCRIPTION_LENGTH = 500


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Task:
    """Modelo de tarea con validación, transiciones de estado y detección de vencimiento."""

    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        self.validate_title(title)
        if due_date is not None:
            self.validate_due_date(due_date)

        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description[:MAX_DESCRIPTION_LENGTH] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # ---------- Validaciones ----------
    @staticmethod
    def validate_title(title):
        if not title or len(title) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_due_date(due_date):
        if due_date < datetime.now():
            raise ValueError("Due date must be in the future")

    # ---------- Estados ----------
    def can_transition(self, new_status):
        """Indica si la transición a new_status es válida."""
        if self.status == TaskStatus.ARCHIVED:
            return False
        if new_status == TaskStatus.ARCHIVED:
            return True

        transitions = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
            TaskStatus.DONE: [],
        }
        return new_status in transitions.get(self.status, [])

    def change_status(self, new_status):
        """Cambia el estado si es válido; si no, lanza ValueError."""
        if not self.can_transition(new_status):
            raise ValueError(
                f"Invalid transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
        self.updated_at = datetime.now()

    def archive(self):
        """Soft delete: marca la tarea como ARCHIVED."""
        self.change_status(TaskStatus.ARCHIVED)

    # ---------- Actualización de campos ----------
    def update(self, title=None, description=None, priority=None, due_date=None):
        """Actualiza campos. No se permite modificar una tarea archivada."""
        if self.status == TaskStatus.ARCHIVED:
            raise ValueError("Cannot modify an archived task")

        if title is not None:
            self.validate_title(title)
            self.title = title
        if description is not None:
            self.description = description[:MAX_DESCRIPTION_LENGTH]
        if priority is not None:
            self.priority = priority
        if due_date is not None:
            self.validate_due_date(due_date)
            self.due_date = due_date

        self.updated_at = datetime.now()

    # ---------- Vencimiento y prioridad ----------
    def is_overdue(self):
        if self.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
            return False
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        """Devuelve 1 si es mayor, -1 si es menor, 0 si es igual."""
        if self.priority.value > other_task.priority.value:
            return 1
        if self.priority.value < other_task.priority.value:
            return -1
        return 0
