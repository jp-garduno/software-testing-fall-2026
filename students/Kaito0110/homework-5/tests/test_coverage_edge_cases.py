
import pytest

from src.task import Task
from src.task_repository import TaskRepository
from src.task_service import TaskService


def test_title_with_surrounding_spaces_is_preserved():
    task = Task(1, "  Study  ")
    assert task.title == "  Study  "


def test_title_with_tabs_only_is_invalid():
    with pytest.raises(ValueError):
        Task(1, "\t\t")


def test_update_title_with_spaces_is_invalid():
    task = Task(1, "Study")

    with pytest.raises(ValueError):
        task.update_title("   ")


def test_empty_repository_returns_empty_list():
    repository = TaskRepository()
    assert repository.get_all() == []


def test_deleted_task_is_not_in_repository():
    repository = TaskRepository()
    repository.add(Task(1, "Study"))
    repository.delete(1)

    assert repository.get_all() == []


def test_completed_task_can_be_completed_again():
    task = Task(1, "Study")
    task.mark_completed()
    task.mark_completed()

    assert task.completed is True


def test_create_task_with_empty_description():
    service = TaskService()
    task = service.create_task(1, "Study", "")

    assert task.description == ""


def test_update_title_twice():
    service = TaskService()
    service.create_task(1, "First")

    service.update_task_title(1, "Second")
    task = service.update_task_title(1, "Third")

    assert task.title == "Third"


def test_complete_task_twice():
    service = TaskService()
    service.create_task(1, "Study")

    service.complete_task(1)
    task = service.complete_task(1)

    assert task.completed is True
    assert service.notifications.sent_notifications.count(
        "Task completed: Study"
    ) == 2


def test_create_task_invalid_priority_does_not_save_task():
    service = TaskService()

    with pytest.raises(ValueError):
        service.create_task(1, "Study", priority="urgent")

    assert service.list_tasks() == []
    assert service.notifications.sent_notifications == []


def test_create_task_invalid_title_does_not_save_task():
    service = TaskService()

    with pytest.raises(ValueError):
        service.create_task(1, "   ")

    assert service.list_tasks() == []
    assert service.notifications.sent_notifications == []


def test_repository_update_keeps_task_count():
    repository = TaskRepository()
    repository.add(Task(1, "First"))
    repository.update(Task(1, "Updated"))

    assert len(repository.get_all()) == 1
    assert repository.get_by_id(1).title == "Updated"
