"""Shared fixtures and test doubles for the TaskFlow suite.

Kinds of test double used in the suite:
- Mock: Mock(spec=...) objects whose calls are verified (repository, notifier, database, HTTP client).
- Stub: those same mocks given canned answers through return_value / side_effect.
- Fake: FakeClock and FakeDatabase, small working implementations.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

import task as task_module
from notification_service import NotificationService
from task_repository import Database, TaskRepository
from task_service import TaskService

FIXED_NOW = datetime(2026, 10, 19, 9, 0)
PHONE = "+523312345678"


class FakeClock:
    """Stands in for task.current_time so every test controls what "now" is."""

    def __init__(self, start):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, **delta):
        """Move time forward, e.g. clock.advance(days=2)."""
        self.now += timedelta(**delta)

    def in_days(self, days):
        """Return the moment that is the given number of days from the current fake time."""
        return self.now + timedelta(days=days)


class FakeDatabase(Database):
    """In-memory implementation of the Database contract."""

    def __init__(self):
        self.records = {}
        self.last_id = 0

    def insert(self, record):
        self.last_id += 1
        self.records[self.last_id] = record
        return self.last_id

    def update(self, record_id, record):
        self.records[record_id] = record

    def get(self, record_id):
        return self.records.get(record_id)

    def get_all(self):
        return list(self.records.values())

    def remove(self, record_id):
        return self.records.pop(record_id, None) is not None


@pytest.fixture(name="clock", autouse=True)
def fixture_clock(monkeypatch):
    """Freeze time in every test, so no result depends on when the suite runs."""
    fake = FakeClock(FIXED_NOW)
    monkeypatch.setattr(task_module, "current_time", fake)
    return fake


@pytest.fixture(name="mock_repository")
def fixture_mock_repository():
    """Repository mock. spec= makes a call to a method TaskRepository lacks fail loudly."""
    repository = Mock(spec=TaskRepository)
    repository.find_by_title.return_value = None
    return repository


@pytest.fixture(name="mock_notifier")
def fixture_mock_notifier():
    return Mock(spec=NotificationService)


@pytest.fixture(name="http_client")
def fixture_http_client():
    """Stub of the HTTP client: the gateway accepts every request and returns a message id."""
    client = Mock()
    client.post.return_value.status_code = 202
    client.post.return_value.json.return_value = {"id": "msg-1"}
    return client


@pytest.fixture(name="notifier")
def fixture_notifier(http_client):
    """The real NotificationService talking to the stubbed HTTP client."""
    return NotificationService(http_client)


@pytest.fixture(name="service")
def fixture_service(mock_repository, mock_notifier):
    """TaskService with both dependencies mocked: no database, no network."""
    return TaskService(mock_repository, mock_notifier, recipient_phone=PHONE)


@pytest.fixture(name="fake_repository")
def fixture_fake_repository():
    """The real TaskRepository on top of an in-memory database."""
    return TaskRepository(FakeDatabase())


@pytest.fixture(name="fake_service")
def fixture_fake_service(fake_repository, mock_notifier):
    """TaskService wired to the real repository; only the external notifier is mocked."""
    return TaskService(fake_repository, mock_notifier, recipient_phone=PHONE)
