from datetime import timedelta

import pytest

from task import Task, TaskPriority, TaskStatus


@pytest.mark.parametrize("action", [
    lambda svc: svc.update_task("missing", title="Title"),
    lambda svc: svc.update_task_status("missing", TaskStatus.DONE),
    lambda svc: svc.delete_task("missing"),
    lambda svc: svc.permanently_delete_task("missing"),
])
def test_missing_tasks(action, service, repository):
    with pytest.raises(ValueError, match="not found"):
        action(service)
    repository.save.assert_not_called()
    repository.delete.assert_not_called()


@pytest.mark.parametrize("changes", [
    {}, {"status": TaskStatus.ARCHIVED}, {"id": "replacement"},
    {"title": "ab"}, {"description": "x" * 501}, {"priority": "HIGH"},
    {"title": "Valid rename", "description": None},
])
def test_invalid_edits_are_atomic(changes, service, repository, clock):
    task = Task("Original", clock=clock)
    repository.find_by_id.return_value = task
    with pytest.raises(ValueError):
        service.update_task(task.id, **changes)
    assert task.title == "Original" and task.description == ""
    repository.save.assert_not_called()


def test_archiving_cannot_modify_fields(service, repository, clock):
    task = Task("Original", clock=clock)
    repository.find_by_id.return_value = task
    with pytest.raises(ValueError):
        service.update_task(task.id, status=TaskStatus.ARCHIVED, title="Renamed")
    repository.save.assert_not_called()


def test_expired_due_date_does_not_block_unrelated_edit(persisted_service, clock):
    task = persisted_service.create_task("Overdue later", due_date=clock() + timedelta(hours=1))
    clock.now += timedelta(days=2)
    assert persisted_service.update_task(task.id, description="Still editable").is_overdue()
    with pytest.raises(ValueError, match="future"):
        persisted_service.update_task(task.id, due_date=clock())
    assert persisted_service.update_task(task.id, due_date=None).due_date is None


@pytest.mark.parametrize("filters", [
    {"status": "TODO"}, {"priority": 10},
    {"start_date": "later", "end_date": "earlier"},
])
def test_invalid_search_filters(filters, service, repository):
    with pytest.raises(ValueError):
        service.search_tasks(**filters)
    repository.find_all.assert_not_called()


def test_date_range_is_inclusive_and_excludes_undated(service, repository, clock):
    tasks = [Task(str(i) + " task", clock=clock) for i in range(5)]
    for i, task in enumerate(tasks[:4]):
        task.due_date = clock() + timedelta(days=i)
    repository.find_all.return_value = tasks
    assert service.search_tasks(start_date=tasks[1].due_date, end_date=tasks[2].due_date) == tasks[1:3]
    assert service.search_tasks(end_date=tasks[1].due_date) == tasks[:2]
    assert service.search_tasks(title="nonexistent") == []
    with pytest.raises(ValueError, match="reversed"):
        service.search_tasks(start_date=tasks[2].due_date, end_date=tasks[1].due_date)


def test_empty_search_and_empty_overdue(service):
    assert service.search_tasks() == []
    assert service.check_overdue_tasks() == []


def test_priority_order_contains_all_levels(persisted_service):
    for priority in TaskPriority:
        persisted_service.create_task(priority.name, priority=priority)
    assert [task.priority for task in persisted_service.search_tasks()] == [
        TaskPriority.URGENT, TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW]
