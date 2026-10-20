"""Shared fixtures and test doubles.

Every test gets fresh objects (function-scoped fixtures), so no state leaks
between tests and they can run in any order.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority
from task_repository import TaskRepository
from task_service import TaskService

# A fixed "current time": tests never depend on the real clock.
NOW = datetime(2026, 10, 19, 12, 0, 0)
TOMORROW = NOW + timedelta(days=1)
NEXT_WEEK = NOW + timedelta(days=7)
PHONE = "+523312345678"


class FakeDatabase:
    """Fake: a tiny working in-memory key/value store with the database interface."""

    def __init__(self):
        self.rows = {}

    def get(self, key):
        return self.rows.get(key)

    def put(self, key, value):
        self.rows[key] = value

    def delete(self, key):
        return self.rows.pop(key, None) is not None

    def values(self):
        return list(self.rows.values())


@pytest.fixture(name="make_task")
def make_task_fixture():
    """Factory for tasks created at NOW (so a due date of TOMORROW is valid)."""

    def _make(title="Write tests", description="", priority=TaskPriority.LOW, due_date=None):
        return Task(title, description, priority, due_date, now=NOW)

    return _make


@pytest.fixture(name="mock_repository")
def mock_repository_fixture():
    """Mock/stub of the repository, restricted to its real interface by spec."""
    repository = Mock(spec=TaskRepository)
    repository.find_by_title.return_value = None
    return repository


@pytest.fixture(name="mock_notification_service")
def mock_notification_service_fixture():
    return Mock(spec=NotificationService)


@pytest.fixture(name="task_service")
def task_service_fixture(mock_repository, mock_notification_service):
    return TaskService(mock_repository, mock_notification_service, clock=lambda: NOW, phone_number=PHONE)


@pytest.fixture(name="fake_database")
def fake_database_fixture():
    return FakeDatabase()


@pytest.fixture(name="fake_repository")
def fake_repository_fixture(fake_database):
    """Real TaskRepository on top of the fake database."""
    return TaskRepository(fake_database)


@pytest.fixture(name="fake_service")
def fake_service_fixture(fake_repository, mock_notification_service):
    """Real service + real repository + fake database; only notifications are mocked."""
    return TaskService(fake_repository, mock_notification_service, clock=lambda: NOW, phone_number=PHONE)
