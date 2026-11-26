"""Unit tests for the Task model. No collaborators: every test builds its own Task."""

from datetime import timedelta

import pytest

from conftest import NOW
from task import (
    DESCRIPTION_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TITLE_MIN_LENGTH,
    InvalidTransitionError,
    Task,
    TaskPriority,
    TaskStatus,
)


def make_task(status=TaskStatus.TODO, priority=TaskPriority.LOW, due_in=None):
    due_date = NOW + due_in if due_in is not None else None
    task = Task("Test task", priority=priority, due_date=due_date, now=NOW)
    task.status = status
    return task


class TestTaskCreation:

    def test_task_creation_with_valid_data(self):
        due_date = NOW + timedelta(days=7)
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date, now=NOW)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == due_date

    def test_task_creation_defaults(self):
        task = Task("Minimal task", now=NOW)

        assert task.description == ""
        assert task.priority == TaskPriority.LOW
        assert task.due_date is None
        assert task.created_at == NOW
        assert task.updated_at == NOW

    def test_none_description_is_stored_as_empty_string(self):
        assert Task("Minimal task", description=None, now=NOW).description == ""

    def test_each_task_gets_a_unique_id(self):
        assert Task("First task", now=NOW).id != Task("Second task", now=NOW).id

    def test_created_at_defaults_to_current_time(self):
        task = Task("Clock task")
        assert task.created_at == task.updated_at

    def test_repr_includes_title_status_and_priority(self):
        text = repr(Task("Repr task", priority=TaskPriority.URGENT, now=NOW))
        assert "Repr task" in text
        assert "TODO" in text
        assert "URGENT" in text


class TestTitleValidation:

    def test_task_creation_with_invalid_title_too_short(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab", now=NOW)

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * (TITLE_MAX_LENGTH + 1), now=NOW)

    @pytest.mark.parametrize("length", [TITLE_MIN_LENGTH, TITLE_MAX_LENGTH])
    def test_title_at_boundary_lengths_is_accepted(self, length):
        assert len(Task("a" * length, now=NOW).title) == length

    @pytest.mark.parametrize("title", ["", None, "   ", "  a  "])
    def test_empty_or_blank_title_is_rejected(self, title):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(title, now=NOW)

    def test_non_string_title_is_rejected(self):
        with pytest.raises(ValueError):
            Task(12345, now=NOW)


class TestDescriptionValidation:

    def test_description_at_max_length_is_accepted(self):
        task = Task("Long description", "d" * DESCRIPTION_MAX_LENGTH, now=NOW)
        assert len(task.description) == DESCRIPTION_MAX_LENGTH

    def test_description_over_max_length_is_rejected(self):
        with pytest.raises(ValueError, match="not exceed 500 characters"):
            Task("Long description", "d" * (DESCRIPTION_MAX_LENGTH + 1), now=NOW)


class TestDueDateValidation:

    def test_task_creation_with_past_due_date(self):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=NOW - timedelta(days=1), now=NOW)

    def test_task_creation_with_due_date_equal_to_now_is_rejected(self):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=NOW, now=NOW)

    def test_task_creation_with_future_due_date(self):
        due_date = NOW + timedelta(seconds=1)
        assert Task("Test task", due_date=due_date, now=NOW).due_date == due_date

    def test_validate_due_date_uses_current_time_by_default(self):
        with pytest.raises(ValueError):
            Task.validate_due_date(NOW)


class TestStatusTransitions:

    def test_can_transition_todo_to_in_progress(self):
        assert make_task(TaskStatus.TODO).can_transition(TaskStatus.IN_PROGRESS)

    def test_can_transition_in_progress_to_done(self):
        assert make_task(TaskStatus.IN_PROGRESS).can_transition(TaskStatus.DONE)

    def test_cannot_transition_done_to_in_progress(self):
        assert not make_task(TaskStatus.DONE).can_transition(TaskStatus.IN_PROGRESS)

    @pytest.mark.parametrize(
        "current, target",
        [
            (TaskStatus.TODO, TaskStatus.DONE),
            (TaskStatus.TODO, TaskStatus.TODO),
            (TaskStatus.IN_PROGRESS, TaskStatus.TODO),
            (TaskStatus.DONE, TaskStatus.TODO),
            (TaskStatus.DONE, TaskStatus.DONE),
        ],
    )
    def test_skipping_backward_or_same_state_transitions_are_invalid(self, current, target):
        assert not make_task(current).can_transition(target)

    @pytest.mark.parametrize("current", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
    def test_can_transition_any_state_to_archived(self, current):
        assert make_task(current).can_transition(TaskStatus.ARCHIVED)

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, target):
        assert not make_task(TaskStatus.ARCHIVED).can_transition(target)

    def test_transition_to_updates_status_and_timestamp(self):
        task = make_task(TaskStatus.TODO)
        later = NOW + timedelta(hours=1)

        old_status = task.transition_to(TaskStatus.IN_PROGRESS, now=later)

        assert old_status == TaskStatus.TODO
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.updated_at == later

    def test_transition_to_invalid_status_raises_and_leaves_task_unchanged(self):
        task = make_task(TaskStatus.DONE)

        with pytest.raises(InvalidTransitionError, match="from DONE to IN_PROGRESS"):
            task.transition_to(TaskStatus.IN_PROGRESS, now=NOW + timedelta(hours=1))

        assert task.status == TaskStatus.DONE
        assert task.updated_at == NOW

    def test_is_archived_property(self):
        assert make_task(TaskStatus.ARCHIVED).is_archived
        assert not make_task(TaskStatus.DONE).is_archived

    def test_touch_defaults_to_current_time(self):
        task = make_task()
        task.touch()
        assert task.updated_at > NOW


class TestOverdueDetection:

    def test_is_overdue_when_past_due_and_not_done(self):
        task = make_task(TaskStatus.TODO, due_in=timedelta(days=1))
        assert task.is_overdue(now=NOW + timedelta(days=2))

    def test_in_progress_task_past_due_is_overdue(self):
        task = make_task(TaskStatus.IN_PROGRESS, due_in=timedelta(days=1))
        assert task.is_overdue(now=NOW + timedelta(days=2))

    def test_is_not_overdue_when_past_due_but_done(self):
        task = make_task(TaskStatus.DONE, due_in=timedelta(days=1))
        assert not task.is_overdue(now=NOW + timedelta(days=2))

    def test_archived_task_is_never_overdue(self):
        task = make_task(TaskStatus.ARCHIVED, due_in=timedelta(days=1))
        assert not task.is_overdue(now=NOW + timedelta(days=2))

    def test_is_not_overdue_when_future_due_date(self):
        task = make_task(TaskStatus.TODO, due_in=timedelta(days=1))
        assert not task.is_overdue(now=NOW)

    def test_is_not_overdue_exactly_at_due_date(self):
        task = make_task(TaskStatus.TODO, due_in=timedelta(days=1))
        assert not task.is_overdue(now=task.due_date)

    def test_task_without_due_date_is_never_overdue(self):
        assert not make_task(TaskStatus.TODO).is_overdue(now=NOW + timedelta(days=365))

    def test_is_overdue_uses_current_time_by_default(self):
        task = make_task(TaskStatus.TODO, due_in=timedelta(days=1))
        task.due_date = NOW - timedelta(days=1)
        assert task.is_overdue()


class TestPriorityComparison:

    def test_priority_comparison_urgent_higher_than_high(self):
        urgent = make_task(priority=TaskPriority.URGENT)
        high = make_task(priority=TaskPriority.HIGH)
        assert urgent.compare_priority(high) == 1

    def test_priority_comparison_low_lower_than_medium(self):
        low = make_task(priority=TaskPriority.LOW)
        medium = make_task(priority=TaskPriority.MEDIUM)
        assert low.compare_priority(medium) == -1

    def test_priority_comparison_equal_priorities(self):
        first = make_task(priority=TaskPriority.HIGH)
        second = make_task(priority=TaskPriority.HIGH)
        assert first.compare_priority(second) == 0

    def test_sorting_orders_urgent_high_medium_low(self):
        tasks = [make_task(priority=p) for p in (TaskPriority.MEDIUM, TaskPriority.LOW,
                                                  TaskPriority.URGENT, TaskPriority.HIGH)]

        ordered = [task.priority for task in sorted(tasks)]

        assert ordered == [TaskPriority.URGENT, TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW]
