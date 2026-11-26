
import pytest

from src.task_service import TaskService
from src.task_repository import TaskRepository
from src.notification_service import NotificationService


@pytest.fixture
def service():
    return TaskService(
        repository=TaskRepository(),
        notifications=NotificationService(),
    )


def test_create_task_and_retrieve_it(service):
    created = service.create_task(1, "Study")
    retrieved = service.get_task(1)

    assert retrieved is created
    assert retrieved.title == "Study"


def test_create_task_sends_notification(service):
    service.create_task(1, "Study")

    assert service.notifications.sent_notifications == [
        "Task created: Study"
    ]


def test_create_task_with_description_and_priority(service):
    task = service.create_task(
        1, "Homework", "Finish testing", "high"
    )

    assert task.description == "Finish testing"
    assert task.priority == "high"


def test_list_tasks(service):
    service.create_task(1, "First")
    service.create_task(2, "Second")

    tasks = service.list_tasks()

    assert len(tasks) == 2
    assert tasks[0].title == "First"
    assert tasks[1].title == "Second"


def test_complete_task_updates_status(service):
    service.create_task(1, "Study")

    task = service.complete_task(1)

    assert task.completed is True
    assert service.get_task(1).completed is True


def test_complete_task_sends_notification(service):
    service.create_task(1, "Study")

    service.complete_task(1)

    assert service.notifications.sent_notifications == [
        "Task created: Study",
        "Task completed: Study",
    ]


def test_update_task_title(service):
    service.create_task(1, "Old title")

    task = service.update_task_title(1, "New title")

    assert task.title == "New title"
    assert service.get_task(1).title == "New title"


def test_delete_task(service):
    service.create_task(1, "Study")

    result = service.delete_task(1)

    assert result is True
    assert service.list_tasks() == []


def test_get_missing_task_raises_error(service):
    with pytest.raises(KeyError):
        service.get_task(99)


def test_complete_missing_task_raises_error(service):
    with pytest.raises(KeyError):
        service.complete_task(99)


def test_update_missing_task_raises_error(service):
    with pytest.raises(KeyError):
        service.update_task_title(99, "New title")


def test_delete_missing_task_raises_error(service):
    with pytest.raises(KeyError):
        service.delete_task(99)


def test_duplicate_task_id_does_not_send_second_notification(service):
    service.create_task(1, "First")

    with pytest.raises(ValueError):
        service.create_task(1, "Duplicate")

    assert service.notifications.sent_notifications == [
        "Task created: First"
    ]
