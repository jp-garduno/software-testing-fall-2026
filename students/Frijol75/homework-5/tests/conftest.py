"""Shared pytest fixtures for unit, integration, and mocking tests."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from unittest.mock import Mock
import pytest

from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


class FakeTaskRepository(TaskRepository):
    """In-memory fake implementation of TaskRepository for testing without external db."""

    def __init__(self):
        super().__init__(database=None)
        self.tasks: Dict[Any, Task] = {}
        self.next_id: int = 1

    def save(self, task: Task) -> Task:
        if task.id is None:
            task.id = self.next_id
            self.next_id += 1
        self.tasks[task.id] = task
        return task

    def find_by_id(self, task_id: Any) -> Optional[Task]:
        return self.tasks.get(task_id)

    def find_by_title(self, title: str) -> Optional[Task]:
        for t in self.tasks.values():
            if t.title == title:
                return t
        return None

    def find_all(self) -> List[Task]:
        return list(self.tasks.values())

    def delete(self, task_id: Any) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


@pytest.fixture
def mock_repository():
    """Mock repository with spec enforcement."""
    return Mock(spec=TaskRepository)


@pytest.fixture
def mock_notification_service():
    """Mock notification service with spec enforcement."""
    return Mock(spec=NotificationService)


@pytest.fixture
def task_service(mock_repository, mock_notification_service):
    """TaskService initialized with mocked dependencies."""
    return TaskService(mock_repository, mock_notification_service)


@pytest.fixture
def sample_task():
    """A valid pre-configured task fixture."""
    due = datetime.now() + timedelta(days=3)
    return Task("Sample Task", "Sample description", TaskPriority.MEDIUM, due, task_id=1)


@pytest.fixture
def fake_repository():
    """In-memory fake repository fixture."""
    return FakeTaskRepository()
