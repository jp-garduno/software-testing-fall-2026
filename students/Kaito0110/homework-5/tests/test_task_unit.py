
import pytest

from src.task import Task
from src.task_repository import TaskRepository


def test_create_task():
    task = Task(1, "Study")
    assert task.title == "Study"


def test_task_default_values():
    task = Task(1, "Study")
    assert task.description == ""
    assert task.completed is False
    assert task.priority == "medium"


def test_create_task_with_all_values():
    task = Task(2, "Homework", "Finish tests", False, "high")
    assert task.description == "Finish tests"
    assert task.priority == "high"


@pytest.mark.parametrize("task_id", [0, -1, -10])
def test_invalid_task_id(task_id):
    with pytest.raises(ValueError):
        Task(task_id, "Study")


@pytest.mark.parametrize("title", ["", "   "])
def test_invalid_task_title(title):
    with pytest.raises(ValueError):
        Task(1, title)


@pytest.mark.parametrize("priority", ["urgent", "normal", ""])
def test_invalid_priority(priority):
    with pytest.raises(ValueError):
        Task(1, "Study", priority=priority)


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_valid_priorities(priority):
    task = Task(1, "Study", priority=priority)
    assert task.priority == priority


def test_mark_task_completed():
    task = Task(1, "Study")
    task.mark_completed()
    assert task.completed is True


def test_update_task_title():
    task = Task(1, "Old title")
    task.update_title("New title")
    assert task.title == "New title"


def test_update_title_with_empty_value():
    task = Task(1, "Study")
    with pytest.raises(ValueError):
        task.update_title("")


def test_repository_add_task():
    repository = TaskRepository()
    task = Task(1, "Study")
    repository.add(task)
    assert repository.get_by_id(1) is task


def test_repository_rejects_duplicate_id():
    repository = TaskRepository()
    repository.add(Task(1, "First"))

    with pytest.raises(ValueError):
        repository.add(Task(1, "Second"))


def test_repository_get_all():
    repository = TaskRepository()
    first = Task(1, "First")
    second = Task(2, "Second")
    repository.add(first)
    repository.add(second)

    assert repository.get_all() == [first, second]


def test_repository_update_task():
    repository = TaskRepository()
    repository.add(Task(1, "Old"))
    updated = Task(1, "New")

    repository.update(updated)

    assert repository.get_by_id(1).title == "New"


def test_repository_update_missing_task():
    repository = TaskRepository()

    with pytest.raises(KeyError):
        repository.update(Task(1, "Missing"))


def test_repository_delete_task():
    repository = TaskRepository()
    repository.add(Task(1, "Study"))

    assert repository.delete(1) is True

    with pytest.raises(KeyError):
        repository.get_by_id(1)


def test_repository_delete_missing_task():
    repository = TaskRepository()

    with pytest.raises(KeyError):
        repository.delete(99)


def test_repository_get_missing_task():
    repository = TaskRepository()

    with pytest.raises(KeyError):
        repository.get_by_id(99)
