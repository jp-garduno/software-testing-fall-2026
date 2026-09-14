import pytest

from src.models import Task, TaskStatus
from src.service import TaskService
from src.validation import TaskValidationError, normalise_tags, validate_priority, validate_title


def test_create_task_assigns_an_identifier_and_normalises_values():
    service = TaskService()

    task = service.create_task("  Review pull request  ", priority=4, tags=["School", "school", " Git "])

    assert task.identifier == 1
    assert task.title == "Review pull request"
    assert task.priority == 4
    assert task.tags == ["school", "git"]
    assert task.status is TaskStatus.OPEN


def test_task_state_methods_and_dictionary_representation():
    task = Task(identifier=7, title="Document findings", priority=2, tags=["docs"])

    assert not task.is_completed
    task.mark_complete()
    assert task.is_completed
    assert task.to_dict() == {
        "id": 7,
        "title": "Document findings",
        "priority": 2,
        "tags": ["docs"],
        "status": "completed",
    }
    task.reopen()

    assert task.status is TaskStatus.OPEN


def test_service_lists_tasks_by_completion_state_and_summarises_them():
    service = TaskService()
    first = service.create_task("Configure hooks")
    second = service.create_task("Run analysis", priority=5)
    service.complete_task(first.identifier)

    assert service.list_tasks() == [first, second]
    assert service.list_tasks(completed=True) == [first]
    assert service.list_tasks(completed=False) == [second]
    assert service.summary() == {"total": 2, "completed": 1, "open": 1}


def test_service_updates_reopens_and_removes_a_task():
    service = TaskService()
    task = service.create_task("Repair warning")
    service.complete_task(task.identifier)

    assert service.reopen_task(task.identifier).is_completed is False
    assert service.update_priority(task.identifier, 1).priority == 1
    assert service.remove_task(task.identifier) == task
    assert service.summary() == {"total": 0, "completed": 0, "open": 0}


def test_unknown_tasks_raise_a_helpful_key_error():
    service = TaskService()

    with pytest.raises(KeyError, match="Task 99 does not exist"):
        service.get_task(99)


@pytest.mark.parametrize("title", ["", "   ", "x" * 81])
def test_validate_title_rejects_empty_or_overlong_text(title):
    with pytest.raises(TaskValidationError):
        validate_title(title)


@pytest.mark.parametrize("priority", [0, 6, True, 2.5, "high"])
def test_validate_priority_rejects_values_outside_the_allowed_range(priority):
    with pytest.raises(TaskValidationError):
        validate_priority(priority)


def test_normalise_tags_handles_none_and_rejects_non_text_tags():
    assert normalise_tags(None) == []

    with pytest.raises(TaskValidationError, match="Every tag must be text"):
        normalise_tags(["valid", 42])
