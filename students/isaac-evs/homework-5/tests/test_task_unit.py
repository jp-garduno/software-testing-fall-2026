"""Unit tests for the Task model. No mocks, files, network or real clock are involved."""

from datetime import timedelta

import pytest

from task import Task, TaskPriority, TaskStatus, sort_by_priority


class TestTaskCreation:
    def test_task_creation_with_valid_data(self, now, future):
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, future, now=now)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == future
        assert task.created_at == now
        assert task.updated_at == now
        assert task.id is None

    def test_task_defaults_are_low_priority_and_no_due_date(self):
        task = Task("Minimal task")

        assert task.priority == TaskPriority.LOW
        assert task.due_date is None
        assert task.description == ""

    def test_task_creation_with_invalid_title_too_short(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_title_at_minimum_length(self):
        assert Task("abc").title == "abc"

    def test_task_creation_with_empty_title(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("")

    def test_task_creation_with_whitespace_only_title(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("     ")

    def test_task_creation_with_non_string_title(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(None)

    def test_task_creation_with_title_at_maximum_length(self):
        assert len(Task("a" * 100).title) == 100

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    def test_task_creation_with_past_due_date(self, now, past):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=past, now=now)

    def test_task_creation_with_due_date_equal_to_now_is_rejected(self, now):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=now, now=now)

    def test_task_creation_with_future_due_date(self, now):
        due = now + timedelta(seconds=1)
        assert Task("Test task", due_date=due, now=now).due_date == due

    def test_task_creation_truncates_description_to_500_characters(self):
        assert len(Task("Test task", "x" * 600).description) == 500

    def test_task_creation_with_invalid_priority(self):
        with pytest.raises(ValueError, match="TaskPriority"):
            Task("Test task", priority="HIGH")

    def test_validate_due_date_uses_real_clock_by_default(self):
        with pytest.raises(ValueError):
            Task.validate_due_date(Task("Other task").created_at - timedelta(days=1))


class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self):
        assert Task("Test task").can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self):
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    @pytest.mark.parametrize("target", [TaskStatus.DONE, TaskStatus.TODO])
    def test_cannot_skip_or_repeat_from_todo(self, target):
        assert Task("Test task").can_transition(target) is False

    @pytest.mark.parametrize("target", [TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    def test_cannot_transition_backwards_from_done(self, target):
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert task.can_transition(target) is False

    def test_cannot_transition_backwards_from_in_progress(self):
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.TODO) is False

    @pytest.mark.parametrize(
        "origin", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
    )
    def test_can_transition_any_open_state_to_archived(self, origin):
        task = Task("Test task")
        task.status = origin
        assert task.can_transition(TaskStatus.ARCHIVED) is True

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, target):
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(target) is False


class TestOverdueDetection:
    def test_is_overdue_when_past_due_and_not_done(self, now, past):
        task = Task("Test task", now=now)
        task.due_date = past
        assert task.is_overdue(now=now) is True

    @pytest.mark.parametrize("status", [TaskStatus.DONE, TaskStatus.ARCHIVED])
    def test_is_not_overdue_when_past_due_but_closed(self, now, past, status):
        task = Task("Test task", now=now)
        task.due_date = past
        task.status = status
        assert task.is_overdue(now=now) is False

    def test_is_not_overdue_when_future_due_date(self, now, future):
        assert Task("Test task", due_date=future, now=now).is_overdue(now=now) is False

    def test_is_not_overdue_when_exactly_at_due_date(self, now):
        task = Task("Test task", now=now)
        task.due_date = now
        assert task.is_overdue(now=now) is False

    def test_is_not_overdue_without_due_date(self, now):
        assert Task("Test task", now=now).is_overdue(now=now) is False

    def test_is_overdue_uses_real_clock_by_default(self, now, past):
        task = Task("Test task", now=now)
        task.due_date = past - timedelta(days=36500)
        assert task.is_overdue() is True


class TestPriority:
    def test_priority_comparison_urgent_higher_than_high(self):
        urgent = Task("Urgent task", priority=TaskPriority.URGENT)
        high = Task("High task", priority=TaskPriority.HIGH)
        assert urgent.compare_priority(high) == 1

    def test_priority_comparison_low_lower_than_medium(self):
        low = Task("Low task", priority=TaskPriority.LOW)
        medium = Task("Medium task", priority=TaskPriority.MEDIUM)
        assert low.compare_priority(medium) == -1

    def test_priority_comparison_equal(self):
        first = Task("First task", priority=TaskPriority.MEDIUM)
        second = Task("Second task", priority=TaskPriority.MEDIUM)
        assert first.compare_priority(second) == 0

    def test_sort_by_priority_orders_urgent_first(self):
        tasks = [
            Task("Low task", priority=TaskPriority.LOW),
            Task("Urgent task", priority=TaskPriority.URGENT),
            Task("Medium task", priority=TaskPriority.MEDIUM),
            Task("High task", priority=TaskPriority.HIGH),
        ]
        ordered = [task.priority for task in sort_by_priority(tasks)]
        assert ordered == [
            TaskPriority.URGENT,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
        ]


class TestHelpers:
    def test_touch_sets_updated_at(self, now):
        task = Task("Test task", now=now)
        later = now + timedelta(hours=1)
        task.touch(later)
        assert task.updated_at == later
        assert task.created_at == now

    def test_touch_defaults_to_real_clock(self, now):
        task = Task("Test task", now=now)
        task.touch()
        assert task.updated_at > now

    def test_repr_includes_title_and_status(self):
        assert "Test task" in repr(Task("Test task"))
        assert "TODO" in repr(Task("Test task"))
