from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from notification_service import NotificationService
from task_repository import TaskRepository
from task_service import TaskService


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
def future():
    return datetime.now() + timedelta(days=7)
