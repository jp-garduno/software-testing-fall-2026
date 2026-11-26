"""Unit tests for the Task model: no repository, no notifier, only the model and a frozen clock."""

import pytest

from task import Task, TaskPriority, TaskStateError, TaskStatus


def task_in(status, due_date=None):
    """Arrange a task directly in the given status, bypassing transitions to isolate the method under test."""
    task = Task("Write unit tests", due_date=due_date)
    task.status = status
    return task


class TestTaskCreation:
    def test_task_creation_with_valid_data(self, clock):
        due_date = clock.in_days(7)
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status is TaskStatus.TODO
        assert task.priority is TaskPriority.HIGH
        assert task.due_date == due_date
        assert task.created_at == clock.now
        assert task.updated_at == task.created_at
        assert task.id is None

    def test_task_creation_applies_defaults(self):
        task = Task("Buy groceries")

        assert (task.description, task.priority, task.due_date) == ("", TaskPriority.LOW, None)

    def test_task_creation_with_invalid_title_too_short(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    @pytest.mark.parametrize("title", ["abc", "a" * 100], ids=["min-3", "max-100"])
    def test_task_creation_accepts_title_length_boundaries(self, title):
        assert Task(title).title == title

    @pytest.mark.parametrize(
        "title", [None, "", "     ", "  ab  ", 42], ids=["none", "empty", "blank", "padded", "int"]
    )
    def test_task_creation_rejects_missing_or_blank_title(self, title):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(title)

    def test_task_creation_strips_title_whitespace(self):
        assert Task("  Plan sprint  ").title == "Plan sprint"

    def test_task_creation_accepts_description_of_500_characters(self):
        assert len(Task("Long notes", "d" * 500).description) == 500

    def test_task_creation_rejects_description_over_500_characters(self):
        with pytest.raises(ValueError, match="Description must not exceed 500"):
            Task("Long notes", "d" * 501)

    def test_task_creation_rejects_priority_that_is_not_an_enum(self):
        with pytest.raises(ValueError, match="TaskPriority"):
            Task("Numeric priority", priority=3)

    @pytest.mark.parametrize("days", [-1, 0], ids=["yesterday", "right-now"])
    def test_task_creation_with_past_due_date(self, clock, days):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Late task", due_date=clock.in_days(days))

    def test_task_creation_with_future_due_date(self, clock):
        due_date = clock.in_days(1)
        assert Task("On time task", due_date=due_date).due_date == due_date


class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self):
        assert task_in(TaskStatus.TODO).can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self):
        assert task_in(TaskStatus.IN_PROGRESS).can_transition(TaskStatus.DONE) is True

    def test_cannot_transition_done_to_in_progress(self):
        assert task_in(TaskStatus.DONE).can_transition(TaskStatus.IN_PROGRESS) is False

    @pytest.mark.parametrize("status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
    def test_can_transition_any_state_to_archived(self, status):
        assert task_in(status).can_transition(TaskStatus.ARCHIVED) is True

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, target):
        assert task_in(TaskStatus.ARCHIVED).can_transition(target) is False

    @pytest.mark.parametrize(
        "current, target",
        [
            (TaskStatus.TODO, TaskStatus.DONE),
            (TaskStatus.TODO, TaskStatus.TODO),
            (TaskStatus.IN_PROGRESS, TaskStatus.TODO),
            (TaskStatus.IN_PROGRESS, TaskStatus.IN_PROGRESS),
            (TaskStatus.DONE, TaskStatus.TODO),
            (TaskStatus.DONE, TaskStatus.DONE),
        ],
    )
    def test_cannot_skip_repeat_or_go_back(self, current, target):
        assert task_in(current).can_transition(target) is False

    def test_transition_to_updates_status_and_returns_previous_one(self, clock):
        task = Task("Move me forward")
        clock.advance(hours=1)

        previous = task.transition_to(TaskStatus.IN_PROGRESS)

        assert previous is TaskStatus.TODO
        assert task.status is TaskStatus.IN_PROGRESS
        assert task.updated_at == clock.now
        assert task.created_at < task.updated_at

    def test_transition_to_invalid_status_raises_and_keeps_state(self, clock):
        task = task_in(TaskStatus.DONE)
        before = task.updated_at
        clock.advance(hours=1)

        with pytest.raises(TaskStateError, match="Invalid transition from DONE to IN_PROGRESS"):
            task.transition_to(TaskStatus.IN_PROGRESS)
        assert task.status is TaskStatus.DONE
        assert task.updated_at == before


class TestTaskUpdate:
    def test_update_changes_fields_and_refreshes_updated_at(self, clock):
        task = Task("Draft report")
        clock.advance(minutes=30)
        new_due_date = clock.in_days(3)

        task.update(
            title=" Final report ", description="Ready for review", priority=TaskPriority.HIGH, due_date=new_due_date
        )

        assert task.title == "Final report"
        assert task.description == "Ready for review"
        assert task.priority is TaskPriority.HIGH
        assert task.due_date == new_due_date
        assert task.updated_at == clock.now

    def test_update_validates_every_field_before_changing_any(self):
        task = Task("Draft report")

        with pytest.raises(ValueError, match="Description"):
            task.update(title="Renamed report", description="x" * 501)
        assert task.title == "Draft report"

    def test_update_without_fields_is_rejected(self):
        with pytest.raises(ValueError, match="No fields to update"):
            Task("Draft report").update()

    def test_update_of_archived_task_is_rejected(self):
        with pytest.raises(TaskStateError, match="Archived tasks cannot be modified"):
            task_in(TaskStatus.ARCHIVED).update(description="too late")


class TestOverdueDetection:
    @pytest.mark.parametrize("status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    def test_is_overdue_when_past_due_and_not_done(self, clock, status):
        task = task_in(status, due_date=clock.in_days(1))
        clock.advance(days=2)
        assert task.is_overdue() is True

    def test_is_not_overdue_when_past_due_but_done(self, clock):
        task = task_in(TaskStatus.DONE, due_date=clock.in_days(1))
        clock.advance(days=2)
        assert task.is_overdue() is False

    def test_is_not_overdue_when_past_due_but_archived(self, clock):
        task = task_in(TaskStatus.ARCHIVED, due_date=clock.in_days(1))
        clock.advance(days=2)
        assert task.is_overdue() is False

    def test_is_not_overdue_when_future_due_date(self, clock):
        assert Task("Plenty of time", due_date=clock.in_days(5)).is_overdue() is False

    def test_is_not_overdue_exactly_at_due_date(self, clock):
        task = Task("Due right now", due_date=clock.in_days(1))
        clock.advance(days=1)
        assert task.is_overdue() is False

    def test_is_not_overdue_without_due_date(self, clock):
        task = Task("Someday")
        clock.advance(days=365)
        assert task.is_overdue() is False


class TestPriorityComparison:
    def test_priority_comparison_urgent_higher_than_high(self):
        assert (
            Task("Outage", priority=TaskPriority.URGENT).compare_priority(Task("Bug", priority=TaskPriority.HIGH)) == 1
        )

    def test_priority_comparison_low_lower_than_medium(self):
        assert (
            Task("Cleanup", priority=TaskPriority.LOW).compare_priority(Task("Docs", priority=TaskPriority.MEDIUM))
            == -1
        )

    def test_priority_comparison_equal_priorities(self):
        assert Task("First").compare_priority(Task("Second")) == 0

    def test_priority_levels_sort_urgent_high_medium_low(self):
        ordered = sorted(TaskPriority, key=lambda priority: priority.value, reverse=True)
        assert ordered == [TaskPriority.URGENT, TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW]
