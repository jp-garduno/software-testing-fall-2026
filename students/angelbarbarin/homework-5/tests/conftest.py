"""Shared fixtures and test doubles for the TaskFlow suite.

Test doubles used across the suite:

* Mock  - ``Mock(spec=...)`` objects whose calls are verified (behaviour).
* Stub  - the same mocks configured with ``return_value`` / ``side_effect`` (data).
* Fake  - ``FakeDatabase``, a small working in-memory database used when we want the
          real TaskRepository logic to run against something that behaves like storage.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority
from task_repository import TaskRepository
from task_service import TaskService


class FakeDatabase:
    """In-memory key/value store with the interface TaskRepository expects."""

    def __init__(self):
        self.rows = {}

    def upsert(self, key, value):
        self.rows[key] = value

    def get(self, key):
        return self.rows.get(key)

    def values(self):
        return list(self.rows.values())

    def remove(self, key):
        return self.rows.pop(key, None) is not None


@pytest.fixture(name="now")
def fixture_now():
    """A fixed reference time so date comparisons are deterministic."""
    return datetime.now()


@pytest.fixture(name="future")
def fixture_future(now):
    return now + timedelta(days=7)


@pytest.fixture(name="make_task")
def fixture_make_task():
    """Factory for valid tasks; keeps test bodies focused on what they check."""

    def _make(title="Write unit tests", priority=TaskPriority.LOW, due_in_days=None, description=""):
        due = datetime.now() + timedelta(days=due_in_days) if due_in_days is not None else None
        return Task(title, description, priority, due)

    return _make


@pytest.fixture(name="mock_repository")
def fixture_mock_repository():
    """Mock repository; by default nothing exists and saves succeed."""
    repo = Mock(spec=TaskRepository)
    repo.find_by_title.return_value = None
    repo.find_by_id.return_value = None
    repo.find_all.return_value = []
    repo.delete.return_value = True
    return repo


@pytest.fixture(name="mock_notifier")
def fixture_mock_notifier():
    return Mock(spec=NotificationService)


@pytest.fixture(name="service")
def fixture_service(mock_repository, mock_notifier):
    """TaskService with both dependencies mocked."""
    return TaskService(mock_repository, mock_notifier, sms_number="+523312345678")


@pytest.fixture(name="fake_db")
def fixture_fake_db():
    return FakeDatabase()


@pytest.fixture(name="repository")
def fixture_repository(fake_db):
    """Real TaskRepository on top of the fake database."""
    return TaskRepository(fake_db)


@pytest.fixture(name="integrated_service")
def fixture_integrated_service(repository, mock_notifier):
    """Real service + real repository + fake DB; only notifications are mocked."""
    return TaskService(repository, mock_notifier)


@pytest.fixture(name="email_client")
def fixture_email_client():
    return Mock(name="email_client")


@pytest.fixture(name="sms_client")
def fixture_sms_client():
    return Mock(name="sms_client")


@pytest.fixture(name="notifier")
def fixture_notifier(email_client, sms_client):
    """Real NotificationService with the external gateways mocked."""
    return NotificationService(email_client, sms_client, max_retries=2)
