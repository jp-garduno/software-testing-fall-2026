"""Shared fixtures for the TaskFlow test suite."""

from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task_repository import TaskRepository
from task_service import TaskService


@pytest.fixture
def mock_repository():
    """Mock of the data layer (no database is ever touched)."""
    return Mock(spec=TaskRepository)


@pytest.fixture
def mock_notification_service():
    """Mock of the external notification provider (no network calls)."""
    return Mock(spec=NotificationService)


@pytest.fixture
def task_service(mock_repository, mock_notification_service):
    return TaskService(mock_repository, mock_notification_service)
