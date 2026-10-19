from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from task import Task, TaskStatus

START = datetime(2026, 10, 19, 9, 0)

LIFECYCLE_PATHS = {
    TaskStatus.TODO: (),
    TaskStatus.IN_PROGRESS: (TaskStatus.IN_PROGRESS,),
    TaskStatus.DONE: (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    TaskStatus.ARCHIVED: (TaskStatus.ARCHIVED,),
}


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


@pytest.fixture
def clock():
    with patch("task.datetime") as patched_datetime:
        yield FrozenClock(patched_datetime)


@pytest.fixture
def make_task():
    """Build a task and walk it through the lifecycle to the requested status."""

    def _make(status=TaskStatus.TODO, title="Write unit tests", **fields):
        task = Task(title, **fields)
        for step in LIFECYCLE_PATHS[status]:
            task.transition_to(step)
        return task

    return _make
