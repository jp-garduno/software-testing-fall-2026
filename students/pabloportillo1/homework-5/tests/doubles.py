from datetime import datetime, timedelta

START = datetime(2026, 10, 19, 9, 0)
OWNER_EMAIL = "owner@taskflow.test"
OWNER_PHONE = "+523312345678"


class FrozenClock:
    """Controls the value task.datetime.now() returns, so every time-based rule is deterministic."""

    def __init__(self, patched_datetime):
        self._patched = patched_datetime
        self._patched.now.return_value = START

    @property
    def now(self):
        return self._patched.now.return_value

    def advance(self, **delta):
        self._patched.now.return_value = self.now + timedelta(**delta)


class FakeDatabase:
    """Working in-memory implementation of the Database protocol, for tests that need real storage."""

    def __init__(self):
        self._rows = {}
        self._next_id = 1

    def insert(self, task):
        task_id = self._next_id
        self._next_id += 1
        self._rows[task_id] = task
        return task_id

    def update(self, task_id, task):
        self._rows[task_id] = task

    def get(self, task_id):
        return self._rows.get(task_id)

    def delete(self, task_id):
        return self._rows.pop(task_id, None) is not None

    def all(self):
        return list(self._rows.values())
