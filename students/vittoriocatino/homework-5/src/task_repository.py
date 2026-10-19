"""Persistence boundary for TaskFlow tasks."""


class TaskRepository:
    """Data access interface; production adapters provide persistence."""

    def __init__(self, database=None):
        """Store an optional database handle for a concrete adapter."""
        self.database = database

    def save(self, task):
        """Persist a task."""
        raise NotImplementedError("Must be implemented by a persistence adapter")

    def find_by_id(self, task_id):
        """Find one task by its identifier."""
        raise NotImplementedError("Must be implemented by a persistence adapter")

    def find_by_title(self, title):
        """Find one task by its exact title."""
        raise NotImplementedError("Must be implemented by a persistence adapter")

    def find_all(self):
        """Return all persisted tasks."""
        raise NotImplementedError("Must be implemented by a persistence adapter")

    def delete(self, task_id):
        """Permanently delete a persisted task when the adapter supports it."""
        raise NotImplementedError("Must be implemented by a persistence adapter")
