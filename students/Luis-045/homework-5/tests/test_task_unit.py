"""Isolated tests for the Task model."""

from datetime import datetime, timedelta, timezone

import pytest

from src.task import Task, TaskPriority, TaskStatus


def test_task_creation_sets_defaults_and_timestamps():
    """A new task starts in TODO with one consistent creation instant."""
    now = datetime(2026, 10, 18, 12, tzinfo=timezone.utc)
    task = Task("Write tests", clock=lambda: now)

    assert task.title == "Write tests"
    assert task.description == ""
    assert task.status is TaskStatus.TODO
    assert task.priority is TaskPriority.LOW
    assert task.due_date is None
    assert task.created_at == task.updated_at == now
    assert isinstance(task.id, str) and task.id


def test_task_creation_preserves_supplied_data():
    """Explicit description, priority and future due date are retained."""
    now = datetime(2026, 10, 18, 12, tzinfo=timezone.utc)
    due_date = now + timedelta(days=7)
    task = Task(
        "Write tests",
        "Practice coverage",
        TaskPriority.HIGH,
        due_date,
        clock=lambda: now,
    )

    assert task.description == "Practice coverage"
    assert task.priority is TaskPriority.HIGH
    assert task.due_date == due_date


@pytest.mark.parametrize("title", [None, 12, "", "ab", " " * 3, "a" * 101])
def test_rejects_invalid_titles(title, clock):
    with pytest.raises(ValueError, match="Title"):
        Task(title, clock=clock)


@pytest.mark.parametrize("length", [3, 100])
def test_accepts_inclusive_title_boundaries(length, clock):
    assert Task("a" * length, clock=clock).title == "a" * length


@pytest.mark.parametrize("description", [42, "a" * 501])
def test_rejects_invalid_descriptions(description, clock):
    with pytest.raises(ValueError, match="Description"):
        Task("Valid title", description=description, clock=clock)


def test_accepts_description_at_maximum_length(clock):
    assert len(Task("Valid title", "a" * 500, clock=clock).description) == 500


def test_none_description_becomes_empty_string(clock):
    assert Task("Valid title", None, clock=clock).description == ""


@pytest.mark.parametrize("priority", [None, 1, "HIGH"])
def test_rejects_priorities_outside_the_enum(priority, clock):
    with pytest.raises(ValueError, match="Priority"):
        Task("Valid title", priority=priority, clock=clock)


@pytest.mark.parametrize("offset", [-1, 0])
def test_rejects_due_dates_not_strictly_in_the_future(offset, clock, now):
    with pytest.raises(ValueError, match="future"):
        Task("Valid title", due_date=now + timedelta(seconds=offset), clock=clock)


@pytest.mark.parametrize("due_date", ["2026-10-20", 123])
def test_rejects_values_that_are_not_datetimes(due_date, clock):
    with pytest.raises(ValueError, match="datetime"):
        Task("Valid title", due_date=due_date, clock=clock)


def test_naive_due_dates_are_interpreted_as_utc(clock, now):
    due_date = (now + timedelta(days=1)).replace(tzinfo=None)
    assert Task(
        "Valid title", due_date=due_date, clock=clock
    ).due_date == now + timedelta(days=1)


@pytest.mark.parametrize("source", list(TaskStatus))
@pytest.mark.parametrize("destination", list(TaskStatus))
def test_all_sixteen_status_transitions(source, destination, clock):
    allowed = {
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.TODO, TaskStatus.ARCHIVED),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.IN_PROGRESS, TaskStatus.ARCHIVED),
        (TaskStatus.DONE, TaskStatus.ARCHIVED),
    }
    task = Task("Valid title", clock=clock)
    task.status = source
    assert task.can_transition(destination) is ((source, destination) in allowed)


def test_unknown_status_is_not_a_valid_transition(clock):
    assert Task("Valid title", clock=clock).can_transition("DONE") is False


@pytest.mark.parametrize("status", list(TaskStatus))
def test_overdue_detection_depends_on_current_state(status, clock, now):
    task = Task("Valid title", due_date=now + timedelta(hours=1), clock=clock)
    task.status = status
    clock.return_value = now + timedelta(hours=2)
    assert task.is_overdue() is (status in (TaskStatus.TODO, TaskStatus.IN_PROGRESS))


def test_task_without_due_date_is_not_overdue(clock):
    assert Task("Valid title", clock=clock).is_overdue() is False


@pytest.mark.parametrize("offset", [0, 1])
def test_due_date_at_or_after_now_is_not_overdue(offset, clock, now):
    task = Task("Valid title", due_date=now + timedelta(hours=1), clock=clock)
    clock.return_value = task.due_date - timedelta(seconds=offset)
    assert task.is_overdue() is False


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (TaskPriority.URGENT, TaskPriority.HIGH, 1),
        (TaskPriority.LOW, TaskPriority.MEDIUM, -1),
        (TaskPriority.HIGH, TaskPriority.HIGH, 0),
    ],
)
def test_priority_comparison_has_three_possible_results(left, right, expected, clock):
    task = Task("First task", priority=left, clock=clock)
    other = Task("Second task", priority=right, clock=clock)
    assert task.compare_priority(other) == expected


def test_tasks_receive_distinct_identities(clock):
    assert Task("First task", clock=clock).id != Task("Second task", clock=clock).id


def test_default_clock_produces_utc_timestamps():
    task = Task("Real clock")
    assert task.created_at.tzinfo is timezone.utc


def test_due_date_validator_can_be_called_directly(clock, now):
    task = Task("Valid title", clock=clock)
    with pytest.raises(ValueError, match="future"):
        task.validate_due_date(now)
