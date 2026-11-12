"""Part 1 - Unit tests for the Task model (no external dependencies at all)."""

from datetime import timedelta
from unittest.mock import patch

import pytest
from conftest import NOW, TOMORROW

from errors import ArchivedTaskError, InvalidTransitionError, TaskValidationError
from task import Task, TaskPriority, TaskStatus


class TestTaskCreation:
    def test_task_creation_with_valid_data(self, make_task):
        task = make_task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, TOMORROW)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == TOMORROW

    def test_task_creation_sets_timestamps_and_id(self, make_task):
        task = make_task()
        assert task.created_at == NOW
        assert task.updated_at == NOW
        assert isinstance(task.task_id, str) and len(task.task_id) == 32

    def test_task_creation_defaults(self, make_task):
        task = make_task()
        assert task.description == ""
        assert task.priority == TaskPriority.LOW
        assert task.due_date is None

    def test_each_task_gets_unique_id(self, make_task):
        assert make_task().task_id != make_task().task_id

    def test_title_is_trimmed(self, make_task):
        assert make_task("  Padded title  ").title == "Padded title"

    @pytest.mark.parametrize("title", ["abc", "a" * 100])
    def test_title_boundaries_are_accepted(self, make_task, title):
        assert make_task(title).title == title

    @pytest.mark.parametrize("title", ["", "ab", "   ", "  ab  ", None, 123])
    def test_task_creation_with_invalid_title_too_short(self, title):
        with pytest.raises(TaskValidationError, match="at least 3 characters"):
            Task(title, now=NOW)

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(TaskValidationError, match="not exceed 100 characters"):
            Task("a" * 101, now=NOW)

    def test_description_of_500_characters_is_accepted(self, make_task):
        assert len(make_task(description="d" * 500).description) == 500

    def test_description_over_500_characters_is_rejected(self):
        with pytest.raises(TaskValidationError, match="Description"):
            Task("Valid title", "d" * 501, now=NOW)

    def test_invalid_priority_is_rejected(self):
        with pytest.raises(TaskValidationError, match="Invalid priority"):
            Task("Valid title", priority="HIGH", now=NOW)

    def test_task_creation_with_past_due_date(self):
        with pytest.raises(TaskValidationError, match="must be in the future"):
            Task("Test task", due_date=NOW - timedelta(days=1), now=NOW)

    def test_due_date_equal_to_now_is_rejected(self):
        with pytest.raises(TaskValidationError, match="must be in the future"):
            Task("Test task", due_date=NOW, now=NOW)

    def test_task_creation_with_future_due_date(self, make_task):
        due = NOW + timedelta(seconds=1)
        assert make_task(due_date=due).due_date == due

    def test_due_date_must_be_datetime(self):
        with pytest.raises(TaskValidationError, match="datetime"):
            Task("Test task", due_date="2030-01-01", now=NOW)

    def test_uses_real_clock_when_now_not_given(self):
        task = Task("Real clock task")
        assert task.created_at == task.updated_at


class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self, make_task):
        assert make_task().can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self, make_task):
        task = make_task()
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    def test_cannot_skip_from_todo_to_done(self, make_task):
        assert make_task().can_transition(TaskStatus.DONE) is False

    def test_cannot_transition_done_to_in_progress(self, make_task):
        task = make_task()
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False

    def test_cannot_transition_to_same_status(self, make_task):
        assert make_task().can_transition(TaskStatus.TODO) is False

    @pytest.mark.parametrize("status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
    def test_can_transition_any_state_to_archived(self, make_task, status):
        task = make_task()
        task.status = status
        assert task.can_transition(TaskStatus.ARCHIVED) is True

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, make_task, target):
        task = make_task()
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(target) is False

    def test_transition_to_updates_status_and_timestamp(self, make_task):
        task = make_task()
        later = NOW + timedelta(hours=1)
        old = task.transition_to(TaskStatus.IN_PROGRESS, now=later)
        assert old == TaskStatus.TODO
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.updated_at == later

    def test_transition_to_invalid_raises_and_keeps_state(self, make_task):
        task = make_task()
        with pytest.raises(InvalidTransitionError, match="Invalid transition from TODO to DONE"):
            task.transition_to(TaskStatus.DONE, now=NOW)
        assert task.status == TaskStatus.TODO
        assert task.updated_at == NOW


class TestTaskUpdate:
    def test_update_changes_fields_and_timestamp(self, make_task):
        task = make_task()
        later = NOW + timedelta(minutes=5)
        task.update(now=later, title=" New title ", description="new", priority=TaskPriority.HIGH)
        assert (task.title, task.description, task.priority) == ("New title", "new", TaskPriority.HIGH)
        assert task.updated_at == later

    def test_update_due_date_must_be_future(self, make_task):
        task = make_task()
        with pytest.raises(TaskValidationError, match="future"):
            task.update(now=NOW, due_date=NOW - timedelta(days=1))

    def test_update_is_atomic_when_one_value_is_invalid(self, make_task):
        task = make_task("Original")
        with pytest.raises(TaskValidationError):
            task.update(now=NOW, description="ok", title="x")
        assert task.title == "Original"
        assert task.description == ""

    def test_update_rejects_unknown_fields(self, make_task):
        with pytest.raises(TaskValidationError, match="status"):
            make_task().update(now=NOW, status=TaskStatus.DONE)

    def test_archived_task_cannot_be_updated(self, make_task):
        task = make_task()
        task.status = TaskStatus.ARCHIVED
        with pytest.raises(ArchivedTaskError):
            task.update(now=NOW, title="Changed")

    def test_touch_without_now_uses_real_clock(self, make_task):
        task = make_task()
        task.touch()
        assert task.updated_at > NOW


class TestOverdueDetection:
    def test_is_overdue_when_past_due_and_not_done(self, make_task):
        task = make_task(due_date=TOMORROW)
        assert task.is_overdue(now=TOMORROW + timedelta(seconds=1)) is True

    def test_is_overdue_when_in_progress(self, make_task):
        task = make_task(due_date=TOMORROW)
        task.status = TaskStatus.IN_PROGRESS
        assert task.is_overdue(now=TOMORROW + timedelta(days=1)) is True

    def test_is_not_overdue_when_past_due_but_done(self, make_task):
        task = make_task(due_date=TOMORROW)
        task.status = TaskStatus.DONE
        assert task.is_overdue(now=TOMORROW + timedelta(days=1)) is False

    def test_is_not_overdue_when_archived(self, make_task):
        task = make_task(due_date=TOMORROW)
        task.status = TaskStatus.ARCHIVED
        assert task.is_overdue(now=TOMORROW + timedelta(days=1)) is False

    def test_is_not_overdue_when_future_due_date(self, make_task):
        assert make_task(due_date=TOMORROW).is_overdue(now=NOW) is False

    def test_is_not_overdue_exactly_at_due_date(self, make_task):
        assert make_task(due_date=TOMORROW).is_overdue(now=TOMORROW) is False

    def test_is_not_overdue_without_due_date(self, make_task):
        assert make_task().is_overdue(now=NOW + timedelta(days=365)) is False

    def test_is_overdue_uses_clock_when_now_not_given(self, make_task):
        task = make_task(due_date=TOMORROW)
        with patch("task.datetime") as fake_datetime:  # mock the clock, not the real time
            fake_datetime.now.return_value = TOMORROW + timedelta(hours=1)
            assert task.is_overdue() is True
            fake_datetime.now.return_value = NOW
            assert task.is_overdue() is False


class TestPriority:
    def test_priority_comparison_urgent_higher_than_high(self, make_task):
        assert make_task(priority=TaskPriority.URGENT).compare_priority(make_task(priority=TaskPriority.HIGH)) == 1

    def test_priority_comparison_low_lower_than_medium(self, make_task):
        assert make_task(priority=TaskPriority.LOW).compare_priority(make_task(priority=TaskPriority.MEDIUM)) == -1

    def test_priority_comparison_equal(self, make_task):
        assert make_task(priority=TaskPriority.HIGH).compare_priority(make_task(priority=TaskPriority.HIGH)) == 0

    def test_sort_key_orders_urgent_high_medium_low(self, make_task):
        tasks = [make_task(f"Task {p.name}", priority=p) for p in TaskPriority]
        ordered = sorted(tasks, key=Task.sort_key)
        assert [t.priority for t in ordered] == [
            TaskPriority.URGENT,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
        ]

    def test_sort_key_ties_broken_by_due_date_then_title(self, make_task):
        no_date = make_task("A no date", priority=TaskPriority.HIGH)
        later = make_task("B later", priority=TaskPriority.HIGH, due_date=NOW + timedelta(days=3))
        sooner = make_task("C sooner", priority=TaskPriority.HIGH, due_date=TOMORROW)
        assert sorted([no_date, later, sooner], key=Task.sort_key) == [sooner, later, no_date]

    def test_repr_is_readable(self, make_task):
        assert repr(make_task("Readable")) == "Task(title='Readable', status=TODO, priority=LOW)"
