from datetime import timedelta
import pytest

from task import Task, TaskPriority, TaskStatus


def test_create_saves_and_notifies(service, repository, notifications, clock):
    task = service.create_task("Write tests", "Homework", TaskPriority.HIGH,
                               clock() + timedelta(days=1))
    assert task.title == "Write tests"
    repository.find_by_title.assert_called_once_with("Write tests")
    repository.save.assert_called_once_with(task)
    notifications.send_email.assert_called_once_with(
        "user@example.com", "New Task Created", "Task 'Write tests' has been created")


def test_duplicate_title_rejected(service, repository, notifications, clock):
    repository.find_by_title.return_value = Task("Duplicate", clock=clock)
    with pytest.raises(ValueError, match="already exists"):
        service.create_task("Duplicate")
    repository.save.assert_not_called()
    notifications.send_email.assert_not_called()


def test_status_change_saves_copy_and_notifies(service, repository, notifications, clock):
    original = Task("Title", clock=clock)
    repository.find_by_id.return_value = original
    clock.now += timedelta(minutes=1)
    updated = service.update_task_status(original.id, TaskStatus.IN_PROGRESS)
    assert updated.status is TaskStatus.IN_PROGRESS
    assert original.status is TaskStatus.TODO
    assert updated.updated_at > original.updated_at
    repository.save.assert_called_once_with(updated)
    notifications.send_email.assert_called_once_with(
        "user@example.com", "Task Status Updated", "Task 'Title' changed from TODO to IN_PROGRESS")


def test_complete_workflow_with_stateful_mock(service, repository, notifications, clock):
    stored = {}
    repository.save.side_effect = lambda task: stored.update({task.id: task})
    repository.find_by_id.side_effect = stored.get
    task = service.create_task("Workflow")
    updated = service.update_task(task.id, description="Edited", priority=TaskPriority.HIGH)
    started = service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    done = service.update_task_status(task.id, TaskStatus.DONE)
    assert done.description == updated.description == "Edited"
    assert started.status is TaskStatus.IN_PROGRESS
    assert done.status is TaskStatus.DONE
    assert repository.save.call_count == 4
    assert notifications.send_email.call_count == 3


def test_archive_is_soft_delete_and_terminal(persisted_service):
    task = persisted_service.create_task("Archive me")
    archived = persisted_service.delete_task(task.id)
    assert persisted_service.repository.find_by_id(task.id).status is TaskStatus.ARCHIVED
    assert archived.status is TaskStatus.ARCHIVED
    with pytest.raises(ValueError, match="Archived"):
        persisted_service.update_task(task.id, title="New name")
    with pytest.raises(ValueError, match="Invalid transition"):
        persisted_service.update_task_status(task.id, TaskStatus.TODO)


def test_invalid_transition_does_not_save(service, repository, notifications, clock):
    task = Task("Finished", clock=clock)
    task.status = TaskStatus.DONE
    repository.find_by_id.return_value = task
    with pytest.raises(ValueError, match="Invalid transition"):
        service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    repository.save.assert_not_called()
    notifications.send_email.assert_not_called()


def test_overdue_check_ignores_terminal_and_future(service, repository, notifications, clock):
    tasks = [Task(str(index) + " task", clock=clock) for index in range(4)]
    for task in tasks:
        task.due_date = clock() - timedelta(days=1)
    tasks[1].status = TaskStatus.DONE
    tasks[2].status = TaskStatus.ARCHIVED
    tasks[3].due_date = clock() + timedelta(days=1)
    repository.find_all.return_value = tasks
    assert service.check_overdue_tasks() == [tasks[0]]
    notifications.send_email.assert_called_once_with(
        "user@example.com", "Task Overdue", "Task '0 task' is overdue")
    notifications.send_sms.assert_not_called()


def test_updates_all_editable_fields(persisted_service, clock):
    task = persisted_service.create_task("Original")
    clock.now += timedelta(hours=1)
    due = clock() + timedelta(days=3)
    updated = persisted_service.update_task(task.id, title="Updated", description="Details",
                                           priority=TaskPriority.URGENT, due_date=due)
    stored = persisted_service.repository.find_by_id(task.id)
    assert (stored.title, stored.description, stored.priority, stored.due_date) == (
        "Updated", "Details", TaskPriority.URGENT, due)
    assert updated.created_at == task.created_at
    assert updated.updated_at == clock()


def test_duplicate_rename_preserves_original(persisted_service):
    first = persisted_service.create_task("First")
    second = persisted_service.create_task("Second")
    with pytest.raises(ValueError, match="already exists"):
        persisted_service.update_task(first.id, title=second.title)
    assert persisted_service.repository.find_by_id(first.id).title == "First"


def test_unchanged_title_is_allowed(persisted_service):
    task = persisted_service.create_task("Same title")
    assert persisted_service.update_task(task.id, title=task.title).title == task.title


def test_permanent_delete_removes_record(persisted_service):
    task = persisted_service.create_task("Delete me")
    persisted_service.permanently_delete_task(task.id)
    assert persisted_service.repository.find_by_id(task.id) is None
    with pytest.raises(ValueError, match="not found"):
        persisted_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)


def test_combined_search_filters_and_sorting(service, repository, clock):
    first = Task("Write report", priority=TaskPriority.HIGH, clock=clock)
    second = Task("Write tests", priority=TaskPriority.URGENT, clock=clock)
    unrelated = Task("Read notes", clock=clock)
    first.due_date = second.due_date = clock() + timedelta(days=2)
    repository.find_all.return_value = [unrelated, first, second]
    assert service.search_tasks() == [second, first, unrelated]
    assert service.search_tasks(status=TaskStatus.TODO, priority=TaskPriority.HIGH,
                                title="WRITE", start_date=clock(),
                                end_date=clock() + timedelta(days=3)) == [first]
    assert service.search_tasks(priority=TaskPriority.URGENT) == [second]
    assert service.search_tasks(status=TaskStatus.DONE) == []


def test_repository_boundaries_with_fake_database(persisted_service):
    task = persisted_service.create_task("Persisted")
    repository = persisted_service.repository
    assert repository.find_by_title(task.title).id == task.id
    assert repository.find_by_title("Missing") is None
    assert [item.id for item in repository.find_all()] == [task.id]
    repository.delete(task.id)
    assert repository.find_all() == []


@pytest.mark.parametrize("operation", ["create", "update", "status", "delete", "overdue", "search"])
def test_database_errors_are_propagated(operation, service, repository, notifications, clock):
    task = Task("Title", clock=clock)
    repository.find_by_id.return_value = task
    repository.save.side_effect = RuntimeError("Database unavailable")
    repository.delete.side_effect = RuntimeError("Database unavailable")
    repository.find_all.side_effect = RuntimeError("Database unavailable")
    actions = {
        "create": lambda: service.create_task("Title"),
        "update": lambda: service.update_task(task.id, title="Updated"),
        "status": lambda: service.update_task_status(task.id, TaskStatus.IN_PROGRESS),
        "delete": lambda: service.permanently_delete_task(task.id),
        "overdue": service.check_overdue_tasks,
        "search": service.search_tasks,
    }
    with pytest.raises(RuntimeError, match="Database unavailable"):
        actions[operation]()
    assert task.title == "Title" and task.status is TaskStatus.TODO
    notifications.send_email.assert_not_called()
