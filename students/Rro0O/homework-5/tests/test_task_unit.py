"""Unit tests for the Task model (fully isolated)."""

# pylint: disable=import-error,redefined-outer-name,unused-argument,too-many-arguments,too-many-positional-arguments

from datetime import datetime, timedelta

import pytest

from task import Task, TaskPriority, TaskStatus


class TestTaskCreation:
    """Test Task Creation."""

    def test_task_creation_with_valid_data(self, future):
        """Test task creation with valid data."""
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, future)
        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == future
        assert task.created_at <= datetime.now()
        assert task.updated_at == task.created_at

    def test_defaults(self):
        """Test defaults."""
        task = Task("Default task")
        assert task.priority == TaskPriority.LOW
        assert task.description == ""
        assert task.due_date is None

    def test_task_creation_with_invalid_title_too_short(self):
        """Test task creation with invalid title too short."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    @pytest.mark.parametrize("title", ["", None])
    def test_task_creation_with_empty_title(self, title):
        """Test task creation with empty title."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(title)

    def test_title_boundary_min_accepted(self):
        """Test title boundary min accepted."""
        assert Task("abc").title == "abc"

    def test_title_boundary_max_accepted(self):
        """Test title boundary max accepted."""
        assert len(Task("a" * 100).title) == 100

    def test_task_creation_with_invalid_title_too_long(self):
        """Test task creation with invalid title too long."""
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    def test_task_creation_with_past_due_date(self, past):
        """Test task creation with past due date."""
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=past)

    def test_task_creation_with_future_due_date(self, future):
        """Test task creation with future due date."""
        assert Task("Test task", due_date=future).due_date == future

    def test_description_truncated_to_500(self):
        """Test description truncated to 500."""
        assert len(Task("Test task", "x" * 600).description) == 500

    def test_none_description_becomes_empty(self):
        """Test none description becomes empty."""
        assert Task("Test task", None).description == ""


class TestStatusTransitions:
    """Test Status Transitions."""

    def test_can_transition_todo_to_in_progress(self):
        """Test can transition todo to in progress."""
        assert Task("Test task").can_transition(TaskStatus.IN_PROGRESS)

    def test_can_transition_in_progress_to_done(self):
        """Test can transition in progress to done."""
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE)

    def test_cannot_skip_todo_to_done(self):
        """Test cannot skip todo to done."""
        assert not Task("Test task").can_transition(TaskStatus.DONE)

    def test_cannot_transition_done_to_in_progress(self):
        """Test cannot transition done to in progress."""
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert not task.can_transition(TaskStatus.IN_PROGRESS)

    @pytest.mark.parametrize("status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
    def test_can_transition_any_state_to_archived(self, status):
        """Test can transition any state to archived."""
        task = Task("Test task")
        task.status = status
        assert task.can_transition(TaskStatus.ARCHIVED)

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, target):
        """Test archived cannot transition to any state."""
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert not task.can_transition(target)


class TestOverdueDetection:
    """Test Overdue Detection."""

    def test_is_overdue_when_past_due_and_not_done(self, past):
        """Test is overdue when past due and not done."""
        task = Task("Test task")
        task.due_date = past
        assert task.is_overdue()

    @pytest.mark.parametrize("status", [TaskStatus.DONE, TaskStatus.ARCHIVED])
    def test_is_not_overdue_when_past_due_but_finished(self, past, status):
        """Test is not overdue when past due but finished."""
        task = Task("Test task")
        task.due_date = past
        task.status = status
        assert not task.is_overdue()

    def test_is_not_overdue_when_future_due_date(self, future):
        """Test is not overdue when future due date."""
        assert not Task("Test task", due_date=future).is_overdue()

    def test_is_not_overdue_without_due_date(self):
        """Test is not overdue without due date."""
        assert not Task("Test task").is_overdue()


class TestPriority:
    """Test Priority."""

    def test_priority_comparison_urgent_higher_than_high(self):
        """Test priority comparison urgent higher than high."""
        urgent = Task("Urgent one", priority=TaskPriority.URGENT)
        high = Task("High one", priority=TaskPriority.HIGH)
        assert urgent.compare_priority(high) == 1

    def test_priority_comparison_low_lower_than_medium(self):
        """Test priority comparison low lower than medium."""
        low = Task("Low one", priority=TaskPriority.LOW)
        medium = Task("Medium one", priority=TaskPriority.MEDIUM)
        assert low.compare_priority(medium) == -1

    def test_priority_comparison_equal(self):
        """Test priority comparison equal."""
        a = Task("First task", priority=TaskPriority.HIGH)
        b = Task("Second task", priority=TaskPriority.HIGH)
        assert a.compare_priority(b) == 0


class TestTouch:  # pylint: disable=too-few-public-methods
    """Test Touch."""

    def test_touch_updates_timestamp(self):
        """Test touch updates timestamp."""
        task = Task("Test task")
        task.updated_at = datetime.now() - timedelta(days=1)
        task.touch()
        assert task.updated_at > task.created_at - timedelta(seconds=1)
        assert datetime.now() - task.updated_at < timedelta(seconds=5)
