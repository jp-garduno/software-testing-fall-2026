"""Data access layer for tasks. The database collaborator is injected so tests can fake it."""


class RepositoryError(Exception):
    """Raised when the underlying database fails."""


class TaskRepository:
    """CRUD and search over a database object exposing save/get/all/remove."""

    def __init__(self, database):
        self.database = database

    def _run(self, operation, *args):
        try:
            return operation(*args)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise RepositoryError(f"Database operation failed: {exc}") from exc

    def save(self, task):
        """Create or update a task and return the stored task."""
        return self._run(self.database.save, task)

    def find_by_id(self, task_id):
        """Return the task with this id, or None."""
        return self._run(self.database.get, task_id)

    def find_by_title(self, title):
        """Return the task with exactly this title (case-insensitive), or None."""
        wanted = title.strip().lower()
        for task in self.find_all():
            if task.title.strip().lower() == wanted:
                return task
        return None

    def find_all(self):
        """Return every stored task."""
        return self._run(self.database.all)

    def delete(self, task_id):
        """Permanently remove a task. Returns True if it existed."""
        return self._run(self.database.remove, task_id)

    def search(
        self,
        status=None,
        priority=None,
        due_from=None,
        due_to=None,
        title_contains=None,
    ):  # pylint: disable=too-many-arguments
        """Return tasks matching ALL of the supplied filters (None means 'ignore')."""
        results = []
        for task in self.find_all():
            if status is not None and task.status != status:
                continue
            if priority is not None and task.priority != priority:
                continue
            if due_from is not None and (task.due_date is None or task.due_date < due_from):
                continue
            if due_to is not None and (task.due_date is None or task.due_date > due_to):
                continue
            if title_contains is not None and title_contains.lower() not in task.title.lower():
                continue
            results.append(task)
        return results
