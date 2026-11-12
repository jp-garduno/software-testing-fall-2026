"""Shared fixtures: mocked dependencies and time helpers."""

# pylint: disable=import-error,redefined-outer-name,unused-argument,too-many-arguments,too-many-positional-arguments

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task_repository import TaskRepository
from task_service import TaskService


@pytest.fixture
def future():
    """A datetime one week ahead."""
    return datetime.now() + timedelta(days=7)


@pytest.fixture
def past():
    """A datetime one day behind."""
    return datetime.now() - timedelta(days=1)


@pytest.fixture
def mock_repository():
    """Mock repository (no title collision by default)."""
    repo = Mock(spec=TaskRepository)
    repo.find_by_title.return_value = None
    return repo


@pytest.fixture
def mock_notification_service():
    """Mock of the external notification API."""
    return Mock(spec=NotificationService)


@pytest.fixture
def task_service(mock_repository, mock_notification_service):
    """TaskService wired to mocks."""
    return TaskService(mock_repository, mock_notification_service)
