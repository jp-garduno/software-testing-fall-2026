"""Focused tests that demonstrate and verify test-double isolation."""

from unittest.mock import Mock

import pytest

from src.notification_service import NotificationService
from src.task import TaskPriority
from src.task_repository import TaskRepository
from src.task_service import TaskService


def test_sms_failure_is_isolated_from_urgent_task_creation():
    repository = Mock(spec=TaskRepository)
    notifications = Mock(spec=NotificationService)
    repository.find_by_title.return_value = None
    notifications.send_sms.side_effect = ConnectionError("SMS provider offline")

    task = TaskService(repository, notifications).create_task(
        "Critical incident", priority=TaskPriority.URGENT
    )

    assert task.title == "Critical incident"
    repository.save.assert_called_once_with(task)
    notifications.send_email.assert_called_once()
    notifications.send_sms.assert_called_once()


def test_mock_specs_prevent_accidental_use_of_nonexistent_dependencies():
    repository = Mock(spec=TaskRepository)

    with pytest.raises(AttributeError):
        repository.drop_everything()
