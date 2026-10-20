from datetime import timedelta, timezone

import pytest

from task import Task, TaskPriority, TaskStatus


def test_task_creation_with_valid_data(clock):
    due = clock() + timedelta(days=7)
    task = Task("Write tests", "Homework", TaskPriority.HIGH, due, clock)
    assert (task.title, task.description, task.priority, task.due_date) == (
        "Write tests", "Homework", TaskPriority.HIGH, due)
    assert task.status is TaskStatus.TODO
    assert task.created_at == task.updated_at == clock()
    assert task.id


def test_defaults_and_unique_identifiers(clock):
    first, second = Task("First", clock=clock), Task("Second", clock=clock)
    assert (first.description, first.priority, first.due_date) == ("", TaskPriority.LOW, None)
    assert first.id != second.id


@pytest.mark.parametrize("title", [None, 123, "", "ab", "a" * 101, "   "])
def test_invalid_titles_are_rejected(title, clock):
    with pytest.raises(ValueError, match="Title"):
        Task(title, clock=clock)


@pytest.mark.parametrize("length", [3, 100])
def test_title_length_boundaries(length, clock):
    assert len(Task("a" * length, clock=clock).title) == length


@pytest.mark.parametrize("description", [None, 45, "a" * 501])
def test_invalid_description(description, clock):
    with pytest.raises(ValueError, match="Description"):
        Task("Title", description=description, clock=clock)


def test_maximum_description_is_preserved(clock):
    assert Task("Title", description="a" * 500, clock=clock).description == "a" * 500


@pytest.mark.parametrize("priority", [None, 1, "HIGH"])
def test_invalid_priority(priority, clock):
    with pytest.raises(ValueError, match="Priority"):
        Task("Title", priority=priority, clock=clock)


@pytest.mark.parametrize("offset", [-1, 0])
def test_due_date_must_be_strictly_future(offset, clock):
    with pytest.raises(ValueError, match="future"):
        Task("Title", due_date=clock() + timedelta(seconds=offset), clock=clock)


@pytest.mark.parametrize("date", ["tomorrow", 12, "aware"])
def test_due_date_requires_local_datetime(date, clock):
    due = clock().replace(tzinfo=timezone.utc) if date == "aware" else date
    with pytest.raises(ValueError, match="naive local datetime"):
        Task("Title", due_date=due, clock=clock)


@pytest.mark.parametrize("old,new", [(old, new) for old in TaskStatus for new in TaskStatus])
def test_every_status_transition(old, new, clock):
    allowed = {
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.TODO, TaskStatus.ARCHIVED),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.IN_PROGRESS, TaskStatus.ARCHIVED),
        (TaskStatus.DONE, TaskStatus.ARCHIVED),
    }
    task = Task("Title", clock=clock)
    task.status = old
    assert task.can_transition(new) is ((old, new) in allowed)


def test_unknown_transition_is_invalid(clock):
    assert not Task("Title", clock=clock).can_transition("DONE")


@pytest.mark.parametrize("status", list(TaskStatus))
@pytest.mark.parametrize("offset", [None, -1, 0, 1])
def test_overdue_boundaries_and_terminal_states(status, offset, clock):
    task = Task("Title", clock=clock)
    task.status = status
    task.due_date = None if offset is None else clock() + timedelta(seconds=offset)
    expected = offset == -1 and status in (TaskStatus.TODO, TaskStatus.IN_PROGRESS)
    assert task.is_overdue() is expected


def test_future_due_date_can_become_overdue(clock):
    task = Task("Title", due_date=clock() + timedelta(days=1), clock=clock)
    assert not task.is_overdue()
    clock.now += timedelta(days=2)
    assert task.is_overdue()


@pytest.mark.parametrize("left,right,expected", [
    (TaskPriority.URGENT, TaskPriority.HIGH, 1),
    (TaskPriority.LOW, TaskPriority.MEDIUM, -1),
    (TaskPriority.HIGH, TaskPriority.HIGH, 0),
])
def test_priority_comparison(left, right, expected, clock):
    assert Task("First", priority=left, clock=clock).compare_priority(
        Task("Second", priority=right, clock=clock)) == expected
