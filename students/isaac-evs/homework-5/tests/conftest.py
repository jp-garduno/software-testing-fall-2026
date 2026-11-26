"""Shared fixtures and test doubles for the TaskFlow test suite."""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task_repository import TaskRepository
from task_service import TaskService


@pytest.fixture
def now():
    """A fixed clock so date-dependent tests never depend on the real time."""
    return datetime(2026, 10, 1, 12, 0, 0)


@pytest.fixture
def future(now):
    """A due date one week after the fixed clock."""
    return now + timedelta(days=7)


@pytest.fixture
def past(now):
    """A date one day before the fixed clock."""
    return now - timedelta(days=1)


class FakeDatabase:
    """Fake: a small but working in-memory database (used where state matters)."""

    def __init__(self):
        self.rows = {}
        self.next_id = 1

    def save(self, task):
        """Store the task, assigning an id on first save."""
        if task.id is None:
            task.id = self.next_id
            self.next_id += 1
        self.rows[task.id] = task
        return task

    def get(self, task_id):
        """Return the task with this id or None."""
        return self.rows.get(task_id)

    def all(self):
        """Return every stored task."""
        return list(self.rows.values())

    def remove(self, task_id):
        """Delete the task; return True if it existed."""
        return self.rows.pop(task_id, None) is not None


@pytest.fixture
def fake_database():
    """A fresh FakeDatabase per test, so tests never share state."""
    return FakeDatabase()


@pytest.fixture
def mock_repository():
    """Mock repository: verifies calls and lets tests stub return values."""
    return Mock(spec=TaskRepository)


@pytest.fixture
def mock_notification_service():
    """Mock notification service: no email or SMS ever leaves the test process."""
    return Mock(spec=NotificationService)


@pytest.fixture
def task_service(mock_repository, mock_notification_service, now):
    """TaskService over mocked collaborators and the fixed clock."""
    return TaskService(mock_repository, mock_notification_service, clock=lambda: now)


@pytest.fixture
def fake_service(fake_database, mock_notification_service, now):
    """TaskService over a real repository backed by the fake database.

    Returns (service, repository, notifier) so tests can inspect all three.
    """
    repository = TaskRepository(fake_database)
    service = TaskService(repository, mock_notification_service, clock=lambda: now)
    return service, repository, mock_notification_service
