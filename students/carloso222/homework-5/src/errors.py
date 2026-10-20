"""Domain exceptions shared by every TaskFlow layer."""


class TaskFlowError(Exception):
    """Base class for every error raised by TaskFlow."""


class TaskValidationError(TaskFlowError, ValueError):
    """A task attribute breaks a validation rule (title, description, due date)."""


class InvalidTransitionError(TaskFlowError, ValueError):
    """A status change does not follow the allowed transition paths."""


class ArchivedTaskError(TaskFlowError, ValueError):
    """An archived task was asked to change; archived is a terminal state."""


class DuplicateTaskError(TaskFlowError, ValueError):
    """Another task already uses the requested title."""


class TaskNotFoundError(TaskFlowError, LookupError):
    """No task exists with the requested id."""


class RepositoryError(TaskFlowError):
    """The persistence layer failed (connection lost, timeout, ...)."""


class NotificationError(TaskFlowError):
    """An email or SMS could not be delivered."""
