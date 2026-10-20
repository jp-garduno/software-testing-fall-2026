
from unittest.mock import Mock

import pytest

from src.task import Task
from src.task_service import TaskService


def test_create_task_calls_repository():
    repository = Mock()
    notifications = Mock()
    service = TaskService(repository, notifications)

    task = service.create_task(1, "Study")

    repository.add.assert_called_once_with(task)


def test_create_task_sends_notification():
    repository = Mock()
    notifications = Mock()
    service = TaskService(repository, notifications)

    task = service.create_task(1, "Study")

    notifications.send_task_created.assert_called_once_with(task)


def test_get_task_uses_repository():
    repository = Mock()
    expected_task = Task(1, "Study")
    repository.get_by_id.return_value = expected_task
    service = TaskService(repository, Mock())

    result = service.get_task(1)

    assert result is expected_task
    repository.get_by_id.assert_called_once_with(1)


def test_list_tasks_uses_repository():
    repository = Mock()
    expected_tasks = [Task(1, "Study"), Task(2, "Homework")]
    repository.get_all.return_value = expected_tasks
    service = TaskService(repository, Mock())

    result = service.list_tasks()

    assert result == expected_tasks
    repository.get_all.assert_called_once_with()


def test_complete_task_updates_repository_and_notifies():
    repository = Mock()
    notifications = Mock()
    task = Task(1, "Study")
    repository.get_by_id.return_value = task
    service = TaskService(repository, notifications)

    result = service.complete_task(1)

    assert result.completed is True
    repository.update.assert_called_once_with(task)
    notifications.send_task_completed.assert_called_once_with(task)


def test_delete_task_uses_repository():
    repository = Mock()
    repository.delete.return_value = True
    service = TaskService(repository, Mock())

    result = service.delete_task(1)

    assert result is True
    repository.delete.assert_called_once_with(1)


def test_invalid_task_does_not_call_repository_or_notification():
    repository = Mock()
    notifications = Mock()
    service = TaskService(repository, notifications)

    with pytest.raises(ValueError):
        service.create_task(1, "   ")

    repository.add.assert_not_called()
    notifications.send_task_created.assert_not_called()


def test_repository_error_prevents_notification():
    repository = Mock()
    notifications = Mock()
    repository.add.side_effect = ValueError("Duplicate ID")
    service = TaskService(repository, notifications)

    with pytest.raises(ValueError, match="Duplicate ID"):
        service.create_task(1, "Study")

    notifications.send_task_created.assert_not_called()
