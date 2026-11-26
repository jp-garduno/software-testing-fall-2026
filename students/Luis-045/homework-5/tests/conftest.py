"""Independent fixtures shared by the TaskFlow test suites."""

from copy import copy
from datetime import datetime, timezone
from unittest.mock import Mock, create_autospec

import pytest

from src.notification_service import NotificationService
from src.task_repository import TaskRepository
from src.task_service import TaskService


@pytest.fixture(name="now")
def fixed_instant():
    """Use a fixed instant so tests do not depend on the machine clock."""
    return datetime(2026, 10, 18, 12, tzinfo=timezone.utc)


@pytest.fixture(name="clock")
def controlled_clock(now):
    """Provide a callable clock whose return value a test can advance."""
    return Mock(return_value=now)


@pytest.fixture(name="mock_repository")
def repository_double():
    """Autospec catches nonexistent methods and incorrect argument counts."""
    repository = create_autospec(TaskRepository, instance=True, spec_set=True)
    repository.find_by_title.return_value = None
    repository.find_by_id.return_value = None
    repository.find_all.return_value = []
    return repository


@pytest.fixture(name="mock_notification")
def notification_double():
    """Replace email and SMS delivery without performing any network calls."""
    return create_autospec(NotificationService, instance=True, spec_set=True)


@pytest.fixture(name="service")
def task_service(mock_repository, mock_notification, clock):
    """Every test receives fresh dependencies and a fresh service."""
    return TaskService(mock_repository, mock_notification, clock=clock)


class FakeTaskRepository:
    """In-memory storage with detached snapshots, used only in workflow tests."""

    def __init__(self):
        self.tasks = {}

    def save(self, task):
        """Persist a snapshot rather than a shared mutable task reference."""
        self.tasks[task.id] = copy(task)

    def find_by_id(self, task_id):
        """Return a detached copy of a stored task."""
        task = self.tasks.get(task_id)
        return copy(task) if task is not None else None

    def find_by_title(self, title):
        """Follow the exact title uniqueness contract."""
        return next((task for task in self.find_all() if task.title == title), None)

    def find_all(self):
        """Return snapshots that cannot mutate storage without save."""
        return [copy(task) for task in self.tasks.values()]

    def delete(self, task_id):
        """Implement the contract; soft deletion must never call this method."""
        del self.tasks[task_id]


@pytest.fixture(name="memory_repository")
def stateful_repository():
    """Keep the fake state independent for every test."""
    return FakeTaskRepository()
