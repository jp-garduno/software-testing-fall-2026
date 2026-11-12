"""Shared fixtures and test doubles for the TaskFlow test suite."""

from datetime import datetime
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task_repository import TaskRepository
from task_service import Recipient, TaskService

# A fixed clock keeps every time-dependent test deterministic.
NOW = datetime(2026, 10, 19, 12, 0, 0)
RECIPIENT = Recipient(email="user@example.com", phone="+523312345678")


class FakeTaskRepository:
    """In-memory fake with the same public interface as TaskRepository."""

    def __init__(self):
        self.tasks = {}

    def save(self, task):
        self.tasks[task.id] = task
        return task

    def find_by_id(self, task_id):
        return self.tasks.get(task_id)

    def find_by_title(self, title):
        return next((task for task in self.tasks.values() if task.title == title), None)

    def find_all(self):
        return list(self.tasks.values())

    def delete(self, task_id):
        return self.tasks.pop(task_id, None) is not None

    def search(self, query):
        return [task for task in self.find_all() if query.matches(task)]


@pytest.fixture(name="mock_repository")
def fixture_mock_repository():
    """Mock with the TaskRepository spec: calling a method that does not exist fails."""
    repository = Mock(spec=TaskRepository)
    repository.find_by_title.return_value = None
    repository.save.side_effect = lambda task: task
    return repository


@pytest.fixture(name="mock_notification_service")
def fixture_mock_notification_service():
    return Mock(spec=NotificationService)


@pytest.fixture(name="task_service")
def fixture_task_service(mock_repository, mock_notification_service):
    return TaskService(mock_repository, mock_notification_service, RECIPIENT, clock=lambda: NOW)


@pytest.fixture(name="fake_repository")
def fixture_fake_repository():
    return FakeTaskRepository()


@pytest.fixture(name="fake_backed_service")
def fixture_fake_backed_service(fake_repository, mock_notification_service):
    return TaskService(fake_repository, mock_notification_service, RECIPIENT, clock=lambda: NOW)
