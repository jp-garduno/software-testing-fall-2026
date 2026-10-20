"""Data access layer for tasks.

The repository talks to a ``database`` object that exposes ``get(key)``,
``put(key, value)``, ``delete(key) -> bool`` and ``values()``. In production
that would be a real database client; in the tests it is replaced by a mock
or by an in-memory fake. Every failure of the database is wrapped in a
``RepositoryError`` so callers only deal with one exception type.
"""

from errors import RepositoryError


class TaskRepository:
    def __init__(self, database):
        self.database = database

    def _execute(self, operation, *args):
        try:
            return getattr(self.database, operation)(*args)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise RepositoryError(f"Database operation '{operation}' failed: {exc}") from exc

    # ------------------------------------------------------------------- CRUD
    def save(self, task):
        """Create or update a task. Returns the saved task."""
        self._execute("put", task.task_id, task)
        return task

    def find_by_id(self, task_id):
        return self._execute("get", task_id)

    def find_by_title(self, title):
        """Exact, case-insensitive title match. Returns the task or None."""
        wanted = title.strip().lower()
        for task in self.find_all():
            if task.title.lower() == wanted:
                return task
        return None

    def find_all(self):
        return list(self._execute("values"))

    def delete(self, task_id):
        """Permanently remove a task. Returns True if something was deleted."""
        return bool(self._execute("delete", task_id))

    # --------------------------------------------------------- search / filter
    def search(  # pylint: disable=too-many-arguments
        self,
        status=None,
        priority=None,
        due_from=None,
        due_to=None,
        title_contains=None,
    ):
        """Return the tasks matching every filter that is given (filters combine with AND).

        ``due_from``/``due_to`` are inclusive; tasks without a due date never match a date filter.
        """
        return [task for task in self.find_all() if _matches(task, status, priority, due_from, due_to, title_contains)]


def _matches(task, status, priority, due_from, due_to, title_contains):  # pylint: disable=too-many-arguments
    return (
        (status is None or task.status == status)
        and (priority is None or task.priority == priority)
        and _in_date_range(task.due_date, due_from, due_to)
        and (not title_contains or title_contains.lower() in task.title.lower())
    )


def _in_date_range(due_date, due_from, due_to):
    if due_from is None and due_to is None:
        return True
    if due_date is None:
        return False
    return (due_from is None or due_date >= due_from) and (due_to is None or due_date <= due_to)
