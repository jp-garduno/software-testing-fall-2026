"""Additional boundary and defensive-path tests for TaskFlow."""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from notification_service import NotificationService
from task import Task, TaskPriority, TaskStatus
from task_repository import TaskRepository
from task_service import TaskService


@pytest.fixture
def boundaries():
    """Create a service and its mock repository for edge-case tests."""
    repository = Mock(spec=TaskRepository)
    return TaskService(repository, Mock(spec=NotificationService)), repository


def test_update_rejects_duplicate_new_title(boundaries):
    """Renaming to another existing title violates uniqueness."""
    service, repository = boundaries
    repository.find_by_id.return_value = Task("Current task")
    repository.find_by_title.return_value = Task("Taken task")
    with pytest.raises(ValueError, match="already exists"):
        service.update_task(1, title="Taken task")


def test_update_rejects_invalid_priority_and_past_date(boundaries):
    """Update validation protects priority type and due-date boundaries."""
    service, repository = boundaries
    repository.find_by_id.return_value = Task("Editable task")
    with pytest.raises(ValueError, match="TaskPriority"):
        service.update_task(1, priority="urgent")
    with pytest.raises(ValueError, match="must be in the future"):
        service.update_task(1, due_date=datetime.now() - timedelta(seconds=1))


def test_search_individual_filters_and_empty_results(boundaries):
    """Each optional search filter handles matching and absent due dates."""
    service, repository = boundaries
    dated = Task(
        "Alpha task",
        priority=TaskPriority.MEDIUM,
        due_date=datetime.now() + timedelta(days=2),
    )
    archived = Task("Beta task", priority=TaskPriority.LOW)
    archived.status = TaskStatus.ARCHIVED
    repository.find_all.return_value = [dated, archived]
    assert service.search_tasks(status=TaskStatus.ARCHIVED) == [archived]
    assert service.search_tasks(priority=TaskPriority.MEDIUM) == [dated]
    assert service.search_tasks(title="ALPHA") == [dated]
    assert service.search_tasks(start_date=datetime.now() + timedelta(days=1)) == [
        dated
    ]
    assert service.search_tasks(end_date=datetime.now() + timedelta(days=1)) == []
