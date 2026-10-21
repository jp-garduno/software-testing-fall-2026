"""Part 1: Unit tests for the Task model (15 isolated tests)."""

from datetime import datetime, timedelta
import pytest

from src.task import Task, TaskPriority, TaskStatus


class TestTaskCreation:
    """Unit tests for Task creation and validation."""

    def test_task_creation_with_valid_data(self):
        """Unit test 1: Create task with valid title and due date."""
        due_date = datetime.now() + timedelta(days=7)
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == due_date

    def test_task_creation_with_invalid_title_too_short(self):
        """Unit test 2: Reject title with fewer than 3 characters."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_invalid_title_too_long(self):
        """Unit test 3: Reject title exceeding 100 characters."""
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    def test_task_creation_with_past_due_date(self):
        """Unit test 4: Reject past due date."""
        past_date = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=past_date)

    def test_task_creation_with_future_due_date(self):
        """Unit test 5: Accept valid future due date and default values."""
        future_date = datetime.now() + timedelta(days=2)
        task = Task("Future task", description="", due_date=future_date)
        assert task.due_date == future_date
        assert task.priority == TaskPriority.LOW
        assert task.description == ""


class TestStatusTransitions:
    """Unit tests for Task status transitions."""

    def test_can_transition_todo_to_in_progress(self):
        """Unit test 6: Valid transition from TODO to IN_PROGRESS."""
        task = Task("Test task")
        assert task.can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self):
        """Unit test 7: Valid transition from IN_PROGRESS to DONE."""
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    def test_cannot_transition_done_to_in_progress(self):
        """Unit test 8: Invalid backward transition from DONE to IN_PROGRESS."""
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False

    def test_can_transition_any_state_to_archived(self):
        """Unit test 9: Can always transition to ARCHIVED from non-archived states."""
        for status in (TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE):
            task = Task("Archive test")
            task.status = status
            assert task.can_transition(TaskStatus.ARCHIVED) is True

    def test_archived_cannot_transition_to_any_state(self):
        """Unit test 10: ARCHIVED is terminal state."""
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(TaskStatus.TODO) is False
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False
        assert task.can_transition(TaskStatus.DONE) is False


class TestOverdueAndPriority:
    """Unit tests for overdue detection and priority comparisons."""

    def test_is_overdue_when_past_due_and_not_done(self):
        """Unit test 11: Task is overdue if past due date and not completed."""
        task = Task("Test task")
        task.due_date = datetime.now() - timedelta(days=1)
        assert task.is_overdue() is True

    def test_is_not_overdue_when_past_due_but_done(self):
        """Unit test 12: Completed tasks are never overdue."""
        task = Task("Test task")
        task.due_date = datetime.now() - timedelta(days=1)
        task.status = TaskStatus.DONE
        assert task.is_overdue() is False

    def test_is_not_overdue_when_future_due_date_or_none(self):
        """Unit test 13: Task with future due date or no due date is not overdue."""
        future_task = Task("Future task", due_date=datetime.now() + timedelta(days=3))
        no_due_task = Task("No due date")
        assert future_task.is_overdue() is False
        assert no_due_task.is_overdue() is False

    def test_priority_comparison_urgent_higher_than_high(self):
        """Unit test 14: URGENT priority is higher than HIGH."""
        urgent = Task("Urgent task", priority=TaskPriority.URGENT)
        high = Task("High task", priority=TaskPriority.HIGH)
        assert urgent.compare_priority(high) == 1

    def test_priority_comparison_low_lower_and_equal(self):
        """Unit test 15: LOW is lower than MEDIUM (-1) and equal to LOW (0)."""
        low1 = Task("Low 1", priority=TaskPriority.LOW)
        low2 = Task("Low 2", priority=TaskPriority.LOW)
        medium = Task("Medium", priority=TaskPriority.MEDIUM)
        assert low1.compare_priority(medium) == -1
        assert low1.compare_priority(low2) == 0
