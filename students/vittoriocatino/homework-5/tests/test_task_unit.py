"""Isolated unit tests for TaskFlow's Task model."""

from datetime import datetime, timedelta

import pytest

from task import Task, TaskPriority, TaskStatus


class TestTaskCreation:
    """Validate Task construction and input rules without external dependencies."""

    def test_creation_with_valid_data(self):
        """A valid task preserves all supplied task data."""
        due_date = datetime.now() + timedelta(days=7)
        task = Task("Write unit tests", "Finish TaskFlow", TaskPriority.HIGH, due_date)
        assert task.title == "Write unit tests"
        assert task.description == "Finish TaskFlow"
        assert task.status is TaskStatus.TODO
        assert task.priority is TaskPriority.HIGH
        assert task.due_date == due_date

    @pytest.mark.parametrize("title", ["", "a", "ab"])
    def test_invalid_short_titles_raise(self, title):
        """Titles shorter than three characters are rejected."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(title)

    def test_invalid_long_title_raises(self):
        """Titles above the maximum length are rejected."""
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    def test_past_due_date_raises(self):
        """Past dates are invalid at task creation time."""
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Future task", due_date=datetime.now() - timedelta(seconds=1))

    def test_invalid_priority_raises(self):
        """Only the TaskPriority enum is accepted as a priority."""
        with pytest.raises(ValueError, match="TaskPriority"):
            Task("Priority task", priority="HIGH")

    def test_description_is_truncated_at_five_hundred_characters(self):
        """Descriptions retain only the documented maximum length."""
        assert len(Task("Long description", description="x" * 501).description) == 500


class TestTaskTransitions:
    """Exercise each valid and invalid lifecycle transition."""

    def test_todo_transitions_to_in_progress(self):
        """TODO can move forward into IN_PROGRESS."""
        assert Task("Transition task").can_transition(TaskStatus.IN_PROGRESS) is True

    def test_in_progress_transitions_to_done(self):
        """IN_PROGRESS can move forward into DONE."""
        task = Task("Transition task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    @pytest.mark.parametrize(
        "status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
    )
    def test_any_active_state_can_archive(self, status):
        """Archiving is always available to active tasks."""
        task = Task("Archive task")
        task.status = status
        assert task.can_transition(TaskStatus.ARCHIVED) is True

    def test_backward_and_skipped_transitions_fail(self):
        """The graph disallows backwards and skipped lifecycle changes."""
        task = Task("Backward task")
        assert task.can_transition(TaskStatus.DONE) is False
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False

    def test_archived_tasks_are_terminal(self):
        """Archived tasks cannot move into any other status."""
        task = Task("Terminal task")
        task.status = TaskStatus.ARCHIVED
        for status in TaskStatus:
            assert task.can_transition(status) is False


class TestTaskOverdueAndPriority:
    """Unit tests for overdue and priority-comparison logic."""

    def test_past_due_active_task_is_overdue(self):
        """Unfinished tasks past their due date are overdue."""
        task = Task("Overdue task")
        task.due_date = datetime.now() - timedelta(days=1)
        assert task.is_overdue() is True

    @pytest.mark.parametrize("status", [TaskStatus.DONE, TaskStatus.ARCHIVED])
    def test_completed_or_archived_tasks_are_not_overdue(self, status):
        """Terminal states suppress overdue notifications."""
        task = Task("Finished task")
        task.due_date = datetime.now() - timedelta(days=1)
        task.status = status
        assert task.is_overdue() is False

    def test_no_due_date_and_future_due_date_are_not_overdue(self):
        """Missing and future dates do not mark an active task overdue."""
        assert Task("No date").is_overdue() is False
        assert (
            Task(
                "Future date", due_date=datetime.now() + timedelta(days=1)
            ).is_overdue()
            is False
        )

    def test_priority_comparison_orders_urgent_high_medium_and_low(self):
        """Priority comparison returns higher, lower, and equal outcomes."""
        urgent = Task("Urgent task", priority=TaskPriority.URGENT)
        high = Task("High task", priority=TaskPriority.HIGH)
        low = Task("Low task", priority=TaskPriority.LOW)
        assert urgent.compare_priority(high) == 1
        assert low.compare_priority(high) == -1
        assert (
            high.compare_priority(Task("Same priority", priority=TaskPriority.HIGH))
            == 0
        )
