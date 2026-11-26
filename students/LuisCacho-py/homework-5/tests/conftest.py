"""Shared pytest fixtures for TaskFlow tests."""
# pylint: disable=redefined-outer-name

from unittest.mock import Mock
import pytest

from src.notification_service import NotificationService
from src.task_repository import TaskRepository
from src.task_service import TaskService


@pytest.fixture
def mock_repository():
    """Create mock repository."""
    return Mock(spec=TaskRepository)


@pytest.fixture
def mock_notification_service():
    """Create mock notification service."""
    return Mock(spec=NotificationService)


@pytest.fixture
def task_service(mock_repository, mock_notification_service):
    """Create TaskService with mocked dependencies."""
    return TaskService(mock_repository, mock_notification_service)
