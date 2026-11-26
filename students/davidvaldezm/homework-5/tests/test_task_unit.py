"""Isolated white-box tests for every Task decision and public behavior."""

from datetime import datetime, timedelta

import pytest

from src.task import Task, TaskPriority, TaskStatus


class TestTaskConstruction:
    def test_creates_a_valid_task_with_default_state(self, future_date):
        task = Task("Write tests", "Cover branches", TaskPriority.HIGH, future_date)

        assert task.title == "Write tests"
        assert task.status is TaskStatus.TODO
        assert task.priority is TaskPriority.HIGH
        assert task.due_date == future_date
        assert task.created_at <= task.updated_at

    @pytest.mark.parametrize("title", ["", "  ", "ab", None])
    def test_rejects_missing_or_short_titles(self, title):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(title)  # type: ignore[arg-type]

    def test_rejects_an_overlong_title(self):
        with pytest.raises(ValueError, match="not exceed 100"):
            Task("t" * 101)

    def test_rejects_an_overlong_description(self):
        with pytest.raises(ValueError, match="Description must not exceed"):
            Task("Valid", "d" * 501)

    def test_rejects_a_non_string_description(self):
        with pytest.raises(ValueError, match="Description must be a string"):
            Task("Valid", 42)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "due_date", [datetime.now() - timedelta(seconds=1), datetime.now()]
    )
    def test_rejects_past_or_current_due_dates(self, due_date):
        with pytest.raises(ValueError, match="future"):
            Task("Valid", due_date=due_date)

    def test_rejects_a_non_datetime_due_date(self):
        with pytest.raises(ValueError, match="datetime"):
            Task("Valid", due_date="tomorrow")  # type: ignore[arg-type]

    def test_rejects_an_invalid_priority(self):
        with pytest.raises(ValueError, match="TaskPriority"):
            Task("Valid", priority=4)  # type: ignore[arg-type]


class TestTaskTransitions:
    def test_allows_normal_forward_transitions(self, task):
        assert task.can_transition(TaskStatus.IN_PROGRESS)
        task.transition_to(TaskStatus.IN_PROGRESS)
        assert task.can_transition(TaskStatus.DONE)
        task.transition_to(TaskStatus.DONE)

        assert task.status is TaskStatus.DONE

    @pytest.mark.parametrize(
        "initial", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
    )
    def test_allows_archiving_from_every_non_terminal_state(self, task, initial):
        task.status = initial

        assert task.can_transition(TaskStatus.ARCHIVED)

    def test_rejects_backward_or_skipped_transitions(self, task):
        assert not task.can_transition(TaskStatus.DONE)
        with pytest.raises(ValueError, match="Invalid transition"):
            task.transition_to(TaskStatus.DONE)

    def test_archived_task_is_terminal(self, task):
        task.status = TaskStatus.ARCHIVED

        assert not task.can_transition(TaskStatus.TODO)
        assert not task.can_transition(TaskStatus.ARCHIVED)

    def test_rejects_a_non_status_transition(self, task):
        assert not task.can_transition("DONE")


class TestTaskBehavior:
    def test_updates_mutable_details_and_refreshes_timestamp(self, task, future_date):
        previous_update = task.updated_at

        task.update_details(
            title="Review results",
            description="Updated description",
            priority=TaskPriority.URGENT,
            due_date=future_date + timedelta(days=1),
        )

        assert (task.title, task.description, task.priority) == (
            "Review results",
            "Updated description",
            TaskPriority.URGENT,
        )
        assert task.updated_at >= previous_update

    def test_rejects_updates_to_archived_task(self, task):
        task.status = TaskStatus.ARCHIVED

        with pytest.raises(ValueError, match="Archived"):
            task.update_details(description="Nope")

    def test_rejects_an_invalid_priority_update(self, task):
        with pytest.raises(ValueError, match="TaskPriority"):
            task.update_details(priority="HIGH")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("status", "due_delta", "expected"),
        [
            (TaskStatus.TODO, -1, True),
            (TaskStatus.IN_PROGRESS, -1, True),
            (TaskStatus.DONE, -1, False),
            (TaskStatus.ARCHIVED, -1, False),
            (TaskStatus.TODO, 1, False),
        ],
    )
    def test_detects_overdue_tasks_for_each_relevant_branch(
        self, task, status, due_delta, expected
    ):
        reference = datetime(2030, 1, 2, 12, 0)
        task.status = status
        task.due_date = reference + timedelta(days=due_delta)

        assert task.is_overdue(reference) is expected

    def test_task_without_due_date_is_not_overdue(self, task):
        task.due_date = None

        assert not task.is_overdue(datetime(2030, 1, 1))

    def test_compares_priority_in_both_directions_and_equal(self):
        low = Task("Low task", priority=TaskPriority.LOW)
        high = Task("High task", priority=TaskPriority.HIGH)
        matching = Task("Other high", priority=TaskPriority.HIGH)

        assert high.compare_priority(low) == 1
        assert low.compare_priority(high) == -1
        assert high.compare_priority(matching) == 0

    def test_rejects_priority_comparison_with_non_task(self, task):
        with pytest.raises(ValueError, match="another Task"):
            task.compare_priority(object())  # type: ignore[arg-type]
