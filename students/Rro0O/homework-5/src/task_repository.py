"""Data access layer for tasks (an interface, mocked in tests)."""


class TaskRepository:
    """Persistence operations; concrete storage is out of scope."""

    def __init__(self, database=None):
        """Init."""
        self.database = database

    def save(self, task):
        """Persist a task."""
        raise NotImplementedError("Must be mocked in tests")

    def find_by_id(self, task_id):
        """Return the task with the given id, or None."""
        raise NotImplementedError("Must be mocked in tests")

    def find_by_title(self, title):
        """Return the task with the exact title, or None."""
        raise NotImplementedError("Must be mocked in tests")

    def find_all(self):
        """Return every stored task."""
        raise NotImplementedError("Must be mocked in tests")

    def delete(self, task_id):
        """Permanently remove a task."""
        raise NotImplementedError("Must be mocked in tests")
