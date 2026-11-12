from datetime import timedelta
from functools import cmp_to_key

import pytest

from task import ArchivedTaskError, InvalidTransitionError, Task, TaskPriority, TaskStatus

ALL_STATUSES = list(TaskStatus)


class TestTaskCreation:
    def test_task_creation_with_valid_data_stores_given_fields(self, clock):
        due_date = clock.now + timedelta(days=7)

        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date)

        assert (task.title, task.description, task.priority, task.due_date) == (
            "Write unit tests",
            "Complete homework 5",
            TaskPriority.HIGH,
            due_date,
        )

    def test_task_creation_starts_in_todo_without_an_id(self):
        task = Task("Write unit tests")

        assert (task.status, task.task_id) == (TaskStatus.TODO, None)

    def test_task_creation_stamps_created_and_updated_at_with_now(self, clock):
        task = Task("Write unit tests")

        assert task.created_at == task.updated_at == clock.now

    def test_task_creation_with_defaults_is_low_priority_without_description_or_due_date(self):
        task = Task("Write unit tests")

        assert (task.priority, task.description, task.due_date) == (TaskPriority.LOW, "", None)

    def test_task_creation_strips_surrounding_whitespace_from_title(self):
        task = Task("   Write unit tests  ")

        assert task.title == "Write unit tests"

    @pytest.mark.parametrize("title", [None, "", "    "])
    def test_task_creation_without_title_is_rejected(self, title):
        with pytest.raises(ValueError, match="Title is required"):
            Task(title)

    def test_task_creation_with_invalid_title_too_short_is_rejected(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_invalid_title_too_long_is_rejected(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    def test_task_creation_with_description_over_500_characters_is_rejected(self):
        with pytest.raises(ValueError, match="not exceed 500 characters"):
            Task("Write unit tests", "d" * 501)

    def test_task_creation_with_none_description_stores_empty_string(self):
        task = Task("Write unit tests", None)

        assert task.description == ""

    @pytest.mark.parametrize("priority", ["HIGH", 3, None])
    def test_task_creation_with_invalid_priority_is_rejected(self, priority):
        with pytest.raises(ValueError, match="Priority must be one of"):
            Task("Write unit tests", priority=priority)

    def test_task_creation_with_past_due_date_is_rejected(self, clock):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Write unit tests", due_date=clock.now - timedelta(days=1))

    def test_task_creation_with_future_due_date_is_accepted(self, clock):
        due_date = clock.now + timedelta(days=1)

        task = Task("Write unit tests", due_date=due_date)

        assert task.due_date == due_date


class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self, make_task):
        assert make_task(TaskStatus.TODO).can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self, make_task):
        assert make_task(TaskStatus.IN_PROGRESS).can_transition(TaskStatus.DONE) is True

    def test_cannot_transition_done_to_in_progress(self, make_task):
        assert make_task(TaskStatus.DONE).can_transition(TaskStatus.IN_PROGRESS) is False

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
    def test_cannot_skip_repeat_or_reverse_a_status(self, make_task, current, target):
        assert make_task(current).can_transition(target) is False

    @pytest.mark.parametrize("current", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
    def test_can_transition_any_state_to_archived(self, make_task, current):
        assert make_task(current).can_transition(TaskStatus.ARCHIVED) is True

    @pytest.mark.parametrize("target", ALL_STATUSES)
    def test_archived_cannot_transition_to_any_state(self, make_task, target):
        assert make_task(TaskStatus.ARCHIVED).can_transition(target) is False

    def test_transition_to_valid_status_changes_status(self, make_task):
        task = make_task(TaskStatus.TODO)

        task.transition_to(TaskStatus.IN_PROGRESS)

        assert task.status == TaskStatus.IN_PROGRESS

    def test_transition_to_stamps_updated_at(self, clock, make_task):
        task = make_task(TaskStatus.TODO)
        clock.advance(hours=3)

        task.transition_to(TaskStatus.IN_PROGRESS)

        assert task.updated_at == clock.now

    def test_transition_to_invalid_status_raises_and_keeps_status(self, make_task):
        task = make_task(TaskStatus.DONE)

        with pytest.raises(InvalidTransitionError, match="from DONE to IN_PROGRESS"):
            task.transition_to(TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.DONE


class TestUpdateDetails:
    def test_update_details_changes_only_the_given_fields(self, make_task):
        task = make_task(description="Original description")

        task.update_details(title="Write integration tests", priority=TaskPriority.URGENT)

        assert (task.title, task.priority, task.description) == (
            "Write integration tests",
            TaskPriority.URGENT,
            "Original description",
        )

    def test_update_details_stamps_updated_at_but_keeps_created_at(self, clock, make_task):
        task = make_task()
        created_at = task.created_at
        clock.advance(days=1)

        task.update_details(description="Now with a description")

        assert (task.created_at, task.updated_at) == (created_at, clock.now)

    def test_update_details_with_one_invalid_value_changes_nothing(self, clock, make_task):
        task = make_task()

        with pytest.raises(ValueError, match="must be in the future"):
            task.update_details(title="Renamed task", due_date=clock.now - timedelta(minutes=1))
        assert task.title == "Write unit tests"

    def test_update_details_on_archived_task_is_rejected(self, make_task):
        task = make_task(TaskStatus.ARCHIVED)

        with pytest.raises(ArchivedTaskError, match="cannot be modified"):
            task.update_details(title="Renamed task")

    def test_update_details_without_changes_keeps_updated_at(self, clock, make_task):
        task = make_task()
        clock.advance(days=1)

        task.update_details()

        assert task.updated_at == task.created_at


class TestOverdueDetection:
    @pytest.mark.parametrize("status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    def test_is_overdue_when_past_due_and_not_done(self, clock, make_task, status):
        task = make_task(status, due_date=clock.now + timedelta(days=1))
        clock.advance(days=2)

        assert task.is_overdue() is True

    def test_is_not_overdue_when_past_due_but_done(self, clock, make_task):
        task = make_task(TaskStatus.DONE, due_date=clock.now + timedelta(days=1))
        clock.advance(days=2)

        assert task.is_overdue() is False

    def test_is_not_overdue_when_past_due_but_archived(self, clock, make_task):
        task = make_task(TaskStatus.ARCHIVED, due_date=clock.now + timedelta(days=1))
        clock.advance(days=2)

        assert task.is_overdue() is False

    def test_is_not_overdue_when_future_due_date(self, clock, make_task):
        task = make_task(due_date=clock.now + timedelta(days=1))

        assert task.is_overdue() is False

    def test_is_not_overdue_without_due_date(self, clock, make_task):
        task = make_task()
        clock.advance(days=365)

        assert task.is_overdue() is False


class TestPriorityComparison:
    def test_priority_comparison_urgent_higher_than_high(self):
        urgent = Task("Fix production bug", priority=TaskPriority.URGENT)
        high = Task("Prepare demo", priority=TaskPriority.HIGH)

        assert urgent.compare_priority(high) == 1

    def test_priority_comparison_low_lower_than_medium(self):
        low = Task("Tidy desk", priority=TaskPriority.LOW)
        medium = Task("Answer emails", priority=TaskPriority.MEDIUM)

        assert low.compare_priority(medium) == -1

    def test_priority_comparison_equal_priorities_returns_zero(self):
        first = Task("Review pull request", priority=TaskPriority.HIGH)
        second = Task("Prepare demo", priority=TaskPriority.HIGH)

        assert first.compare_priority(second) == 0

    def test_priority_comparison_orders_urgent_high_medium_low(self):
        tasks = [Task(f"Task {priority.name}", priority=priority) for priority in TaskPriority]

        ordered = sorted(tasks, key=cmp_to_key(Task.compare_priority), reverse=True)

        assert [task.priority for task in ordered] == [
            TaskPriority.URGENT,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
        ]
