"""Unit tests for the Task model.

Every test builds its own Task and touches no repository, database or network, so
the model is tested in complete isolation.
"""

from datetime import datetime, timedelta

import pytest

from task import InvalidTransitionError, Task, TaskPriority, TaskStatus, TaskValidationError


class TestTaskCreation:
    def test_task_creation_with_valid_data(self, future):
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, future)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == future

    def test_task_creation_defaults(self):
        task = Task("Buy milk")

        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.LOW
        assert task.description == ""
        assert task.due_date is None

    def test_task_creation_sets_timestamps_and_unique_id(self):
        before = datetime.now()
        first = Task("First task")
        second = Task("Second task")

        assert before <= first.created_at <= datetime.now()
        assert first.updated_at == first.created_at
        assert first.id != second.id

    def test_task_creation_with_future_due_date(self):
        due = datetime.now() + timedelta(minutes=1)
        assert Task("Soon due", due_date=due).due_date == due

    def test_task_creation_with_past_due_date(self):
        with pytest.raises(TaskValidationError, match="must be in the future"):
            Task("Late task", due_date=datetime.now() - timedelta(days=1))

    def test_task_creation_with_non_datetime_due_date(self):
        with pytest.raises(TaskValidationError, match="must be a datetime"):
            Task("Bad due date", due_date="2030-01-01")


class TestTitleValidation:
    @pytest.mark.parametrize("title", ["abc", "a" * 100, "  abc  "])
    def test_title_on_valid_boundaries_is_accepted(self, title):
        assert Task(title).title == title

    def test_task_creation_with_invalid_title_too_short(self):
        with pytest.raises(TaskValidationError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(TaskValidationError, match="not exceed 100 characters"):
            Task("a" * 101)

    @pytest.mark.parametrize("title", ["", "   ", None, 123])
    def test_missing_or_non_string_title_is_rejected(self, title):
        with pytest.raises(TaskValidationError, match="Title is required"):
            Task(title)

    def test_title_only_spaces_around_two_chars_is_too_short(self):
        with pytest.raises(TaskValidationError, match="at least 3"):
            Task("  ab  ")


class TestDescriptionAndPriorityValidation:
    def test_description_at_500_characters_is_accepted(self):
        assert len(Task("Long notes", "x" * 500).description) == 500

    def test_description_over_500_characters_is_rejected(self):
        with pytest.raises(TaskValidationError, match="not exceed 500"):
            Task("Long notes", "x" * 501)

    def test_description_none_becomes_empty_string(self):
        assert Task("No notes", None).description == ""

    def test_description_non_string_is_rejected(self):
        with pytest.raises(TaskValidationError, match="must be a string"):
            Task("Bad notes", 42)

    def test_invalid_priority_is_rejected(self):
        with pytest.raises(TaskValidationError, match="Invalid priority"):
            Task("Bad priority", priority=3)


class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self):
        assert Task("Test task").can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self):
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    def test_cannot_skip_from_todo_to_done(self):
        assert Task("Test task").can_transition(TaskStatus.DONE) is False

    def test_cannot_transition_done_to_in_progress(self):
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False

    def test_cannot_transition_to_same_status(self):
        assert Task("Test task").can_transition(TaskStatus.TODO) is False

    @pytest.mark.parametrize("status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
    def test_can_transition_any_state_to_archived(self, status):
        task = Task("Test task")
        task.status = status
        assert task.can_transition(TaskStatus.ARCHIVED) is True

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, target):
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(target) is False

    def test_transition_to_changes_status_and_returns_previous(self):
        task = Task("Test task")
        old_updated = task.updated_at

        previous = task.transition_to(TaskStatus.IN_PROGRESS)

        assert previous == TaskStatus.TODO
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.updated_at >= old_updated

    def test_transition_to_invalid_status_raises(self):
        task = Task("Test task")
        with pytest.raises(InvalidTransitionError, match="Invalid transition from TODO to DONE"):
            task.transition_to(TaskStatus.DONE)
        assert task.status == TaskStatus.TODO

    def test_transition_to_unknown_value_raises(self):
        with pytest.raises(InvalidTransitionError, match="Unknown status"):
            Task("Test task").transition_to("DONE")

    def test_is_archived_property(self):
        task = Task("Test task")
        assert task.is_archived is False
        task.transition_to(TaskStatus.ARCHIVED)
        assert task.is_archived is True


class TestUpdateFields:
    def test_update_fields_changes_values_and_reports_them(self, future):
        task = Task("Old title")

        changed = task.update_fields(
            title="New title", description="notes", priority=TaskPriority.HIGH, due_date=future
        )

        assert changed == ["title", "description", "priority", "due_date"]
        assert (task.title, task.description, task.priority, task.due_date) == (
            "New title",
            "notes",
            TaskPriority.HIGH,
            future,
        )

    def test_update_fields_with_same_values_changes_nothing(self):
        task = Task("Same title")
        old_updated = task.updated_at

        assert task.update_fields(title="Same title") == []
        assert task.updated_at == old_updated

    def test_update_fields_with_no_arguments_changes_nothing(self):
        assert Task("Same title").update_fields() == []

    def test_update_fields_is_atomic_when_one_value_is_invalid(self):
        task = Task("Old title")

        with pytest.raises(TaskValidationError):
            task.update_fields(title="New title", due_date=datetime.now() - timedelta(days=1))

        assert task.title == "Old title"

    def test_update_fields_on_archived_task_raises(self):
        task = Task("Old title")
        task.transition_to(TaskStatus.ARCHIVED)
        with pytest.raises(InvalidTransitionError, match="Archived tasks cannot be modified"):
            task.update_fields(title="New title")


class TestOverdueDetection:
    def test_is_overdue_when_past_due_and_not_done(self, now):
        task = Task("Test task", due_date=now + timedelta(hours=1))
        assert task.is_overdue(now + timedelta(hours=2)) is True

    def test_is_overdue_when_in_progress_and_past_due(self, now):
        task = Task("Test task", due_date=now + timedelta(hours=1))
        task.status = TaskStatus.IN_PROGRESS
        assert task.is_overdue(now + timedelta(hours=2)) is True

    def test_is_not_overdue_when_past_due_but_done(self, now):
        task = Task("Test task", due_date=now + timedelta(hours=1))
        task.status = TaskStatus.DONE
        assert task.is_overdue(now + timedelta(hours=2)) is False

    def test_is_not_overdue_when_past_due_but_archived(self, now):
        task = Task("Test task", due_date=now + timedelta(hours=1))
        task.status = TaskStatus.ARCHIVED
        assert task.is_overdue(now + timedelta(hours=2)) is False

    def test_is_not_overdue_when_future_due_date(self, future):
        assert Task("Test task", due_date=future).is_overdue() is False

    def test_is_not_overdue_without_due_date(self):
        assert Task("Test task").is_overdue() is False

    def test_is_not_overdue_exactly_at_due_date(self, now):
        due = now + timedelta(hours=1)
        assert Task("Test task", due_date=due).is_overdue(due) is False

    def test_is_overdue_uses_current_time_by_default(self):
        task = Task("Test task", due_date=datetime.now() + timedelta(days=1))
        task.due_date = datetime.now() - timedelta(seconds=1)  # set after creation to bypass validation
        assert task.is_overdue() is True


class TestPriorityComparison:
    def test_priority_comparison_urgent_higher_than_high(self):
        assert (
            Task("Urgent", priority=TaskPriority.URGENT).compare_priority(Task("High", priority=TaskPriority.HIGH)) == 1
        )

    def test_priority_comparison_low_lower_than_medium(self):
        assert (
            Task("Low", priority=TaskPriority.LOW).compare_priority(Task("Medium", priority=TaskPriority.MEDIUM)) == -1
        )

    def test_priority_comparison_equal(self):
        assert Task("One", priority=TaskPriority.HIGH).compare_priority(Task("Two", priority=TaskPriority.HIGH)) == 0

    def test_sorting_puts_urgent_first(self, make_task):
        tasks = [make_task(f"Task {p.name}", priority=p) for p in TaskPriority]

        ordered = sorted(tasks, reverse=True)

        assert [t.priority for t in ordered] == [
            TaskPriority.URGENT,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
        ]

    def test_repr_contains_title_and_status(self):
        assert "Readable" in repr(Task("Readable")) and "TODO" in repr(Task("Readable"))
