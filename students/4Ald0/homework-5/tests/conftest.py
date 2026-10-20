from copy import deepcopy
from datetime import datetime
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task_repository import TaskRepository
from task_service import TaskService


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 19, 12)

    def __call__(self):
        return self.now


class FakeDatabase:
    """In-memory test double with copy semantics resembling persistence."""
    def __init__(self):
        self.tasks = {}

    def save(self, task):
        self.tasks[task.id] = deepcopy(task)

    def find_by_id(self, task_id):
        return deepcopy(self.tasks.get(task_id))

    def find_all(self):
        return deepcopy(list(self.tasks.values()))

    def delete(self, task_id):
        del self.tasks[task_id]


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def repository():
    repository = Mock(spec=TaskRepository)
    repository.find_by_title.return_value = None
    repository.find_by_id.return_value = None
    repository.find_all.return_value = []
    return repository


@pytest.fixture
def notifications():
    return Mock(spec=NotificationService)


@pytest.fixture
def service(repository, notifications, clock):
    return TaskService(repository, notifications, clock=clock)


@pytest.fixture
def persisted_service(clock, notifications):
    return TaskService(TaskRepository(FakeDatabase()), notifications, clock=clock)
