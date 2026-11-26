"""Data access layer for tasks (to be mocked in tests)."""


class TaskRepository:
    """Data access layer for tasks."""

    def __init__(self, database=None):
        self.database = database

    def save(self, task):
        """Save task to database."""
        raise NotImplementedError("Must be mocked in tests")

    def find_by_id(self, task_id):
        """Find task by ID."""
        raise NotImplementedError("Must be mocked in tests")

    def find_by_title(self, title):
        """Find task by exact title."""
        raise NotImplementedError("Must be mocked in tests")

    def find_all(self):
        """Get all tasks."""
        raise NotImplementedError("Must be mocked in tests")

    def delete(self, task_id):
        """Delete task."""
        raise NotImplementedError("Must be mocked in tests")
