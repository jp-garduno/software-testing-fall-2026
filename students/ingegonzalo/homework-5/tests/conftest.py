from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


class FakeTaskRepository:
    """Fake: simplified but working in-memory implementation."""

    def __init__(self):
        self.tasks = {}
        self._next_id = 1

    def save(self, task):
        if task.id is None:
            task.id = self._next_id
            self._next_id += 1
        self.tasks[task.id] = task
        return task

    def find_by_id(self, task_id):
        return self.tasks.get(task_id)

    def find_by_title(self, title):
        return next((t for t in self.tasks.values() if t.title == title), None)

    def find_all(self):
        return list(self.tasks.values())

    def delete(self, task_id):
        return self.tasks.pop(task_id, None) is not None


@pytest.fixture
def mock_repository():
    return Mock(spec=TaskRepository)


@pytest.fixture
def mock_notification_service():
    return Mock(spec=NotificationService)


@pytest.fixture
def task_service(mock_repository, mock_notification_service):
    return TaskService(mock_repository, mock_notification_service)


@pytest.fixture
def fake_repository():
    return FakeTaskRepository()


@pytest.fixture
def make_task():
    """Factory that builds tasks in any state, bypassing validation on purpose."""
    def _make(title="Sample task", status=TaskStatus.TODO,
              priority=TaskPriority.LOW, due_date=None):
        task = Task(title, priority=priority)
        task.status = status
        task.due_date = due_date
        return task
    return _make