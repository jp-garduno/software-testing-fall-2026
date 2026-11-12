"""Unit tests for the Task model.

Every test is fully isolated: no repository, no notification service, no I/O.
"""

from datetime import datetime, timedelta

import pytest

from task import Task, TaskPriority, TaskStatus


def future(days=7):
    return datetime.now() + timedelta(days=days)


def past(days=1):
    return datetime.now() - timedelta(days=days)


class TestTaskCreation:
    def test_task_creation_with_valid_data(self):
        due_date = future()
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == due_date
        assert task.id is None

    def test_task_creation_uses_defaults(self):
        task = Task("Defaults")

        assert task.description == ""
        assert task.priority == TaskPriority.LOW
        assert task.due_date is None

    def test_task_creation_sets_timestamps(self):
        before = datetime.now()
        task = Task("Timestamps")
        after = datetime.now()

        assert before <= task.created_at <= after
        assert task.updated_at == task.created_at

    def test_task_creation_with_future_due_date(self):
        task = Task("Future task", due_date=future(1))
        assert task.due_date > datetime.now()

    def test_task_creation_with_past_due_date(self):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=past())

    def test_description_is_truncated_to_500_characters(self):
        task = Task("Long description", "x" * 600)
        assert len(task.description) == 500

    def test_none_description_becomes_empty_string(self):
        task = Task("No description", None)
        assert task.description == ""


class TestTitleValidation:
    def test_task_creation_with_invalid_title_too_short(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_empty_title(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("")

    def test_task_creation_with_none_title(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(None)

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    @pytest.mark.parametrize("length", [3, 100])
    def test_title_boundary_lengths_are_accepted(self, length):
        assert Task("a" * length).title == "a" * length


class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self):
        assert Task("Test task").can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self):
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    def test_cannot_skip_todo_to_done(self):
        assert Task("Test task").can_transition(TaskStatus.DONE) is False

    def test_cannot_transition_done_to_in_progress(self):
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False

    def test_cannot_transition_to_same_status(self):
        assert Task("Test task").can_transition(TaskStatus.TODO) is False

    @pytest.mark.parametrize(
        "status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
    )
    def test_can_transition_any_state_to_archived(self, status):
        task = Task("Test task")
        task.status = status
        assert task.can_transition(TaskStatus.ARCHIVED) is True

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, target):
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(target) is False


class TestOverdueDetection:
    def test_is_overdue_when_past_due_and_not_done(self):
        task = Task("Test task")
        task.due_date = past()
        assert task.is_overdue() is True

    def test_is_overdue_when_in_progress_and_past_due(self):
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        task.due_date = past()
        assert task.is_overdue() is True

    def test_is_not_overdue_when_past_due_but_done(self):
        task = Task("Test task")
        task.due_date = past()
        task.status = TaskStatus.DONE
        assert task.is_overdue() is False

    def test_is_not_overdue_when_past_due_but_archived(self):
        task = Task("Test task")
        task.due_date = past()
        task.status = TaskStatus.ARCHIVED
        assert task.is_overdue() is False

    def test_is_not_overdue_when_future_due_date(self):
        assert Task("Test task", due_date=future()).is_overdue() is False

    def test_is_not_overdue_without_due_date(self):
        assert Task("Test task").is_overdue() is False


class TestPriorityComparison:
    def test_priority_comparison_urgent_higher_than_high(self):
        urgent = Task("Urgent", priority=TaskPriority.URGENT)
        high = Task("High", priority=TaskPriority.HIGH)
        assert urgent.compare_priority(high) == 1

    def test_priority_comparison_low_lower_than_medium(self):
        low = Task("Low", priority=TaskPriority.LOW)
        medium = Task("Medium", priority=TaskPriority.MEDIUM)
        assert low.compare_priority(medium) == -1

    def test_priority_comparison_equal(self):
        a = Task("First", priority=TaskPriority.MEDIUM)
        b = Task("Second", priority=TaskPriority.MEDIUM)
        assert a.compare_priority(b) == 0

    def test_sorting_follows_urgent_high_medium_low(self):
        tasks = [Task(p.name.title() + " one", priority=p) for p in TaskPriority]
        ordered = sorted(tasks, key=lambda t: t.priority.value, reverse=True)
        assert [t.priority for t in ordered] == [
            TaskPriority.URGENT,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
        ]


class TestHelpers:
    def test_touch_updates_updated_at(self):
        task = Task("Touch me")
        task.updated_at = past(2)
        task.touch()
        assert task.updated_at > past(1)

    def test_repr_contains_title_and_status(self):
        text = repr(Task("Readable"))
        assert "Readable" in text and "TODO" in text
