from datetime import datetime, timedelta

import pytest

from task import Task, TaskPriority, TaskStatus


class TestTaskCreation:
    def test_creation_with_valid_data(self):
        due = datetime.now() + timedelta(days=7)
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due)
        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == due

    def test_creation_defaults(self):
        task = Task("Default task")
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.LOW
        assert task.due_date is None
        assert task.description == ""
        assert task.id is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    @pytest.mark.parametrize("bad_title", [None, "", "ab"])
    def test_creation_with_invalid_title_too_short(self, bad_title):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(bad_title)

    def test_creation_with_invalid_title_too_long(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    @pytest.mark.parametrize("length", [3, 100])
    def test_creation_with_boundary_title_lengths(self, length):
        assert len(Task("a" * length).title) == length

    def test_description_is_truncated_to_500_chars(self):
        assert len(Task("Long desc", "x" * 600).description) == 500

    def test_none_description_becomes_empty_string(self):
        assert Task("No desc", description=None).description == ""

    def test_creation_with_past_due_date(self):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=datetime.now() - timedelta(days=1))

    def test_creation_with_future_due_date(self):
        due = datetime.now() + timedelta(days=1)
        assert Task("Test task", due_date=due).due_date == due


class TestStatusTransitions:
    @pytest.mark.parametrize("current,target", [
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    ])
    def test_valid_forward_transitions(self, current, target):
        task = Task("Test task")
        task.status = current
        assert task.can_transition(target) is True

    @pytest.mark.parametrize("current,target", [
        (TaskStatus.TODO, TaskStatus.DONE),
        (TaskStatus.TODO, TaskStatus.TODO),
        (TaskStatus.IN_PROGRESS, TaskStatus.TODO),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
        (TaskStatus.DONE, TaskStatus.TODO),
    ])
    def test_invalid_transitions(self, current, target):
        task = Task("Test task")
        task.status = current
        assert task.can_transition(target) is False

    @pytest.mark.parametrize("current", [
        TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE,
    ])
    def test_any_state_can_transition_to_archived(self, current):
        task = Task("Test task")
        task.status = current
        assert task.can_transition(TaskStatus.ARCHIVED) is True

    @pytest.mark.parametrize("target", list(TaskStatus))
    def test_archived_cannot_transition_to_any_state(self, target):
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(target) is False


class TestOverdueDetection:
    def test_is_overdue_when_past_due_and_not_done(self):
        task = Task("Test task")
        task.due_date = datetime.now() - timedelta(days=1)
        assert task.is_overdue() is True

    def test_is_overdue_when_in_progress(self):
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        task.due_date = datetime.now() - timedelta(hours=1)
        assert task.is_overdue() is True

    def test_is_not_overdue_when_past_due_but_done(self):
        task = Task("Test task")
        task.due_date = datetime.now() - timedelta(days=1)
        task.status = TaskStatus.DONE
        assert task.is_overdue() is False

    def test_is_not_overdue_when_archived(self):
        task = Task("Test task")
        task.due_date = datetime.now() - timedelta(days=1)
        task.status = TaskStatus.ARCHIVED
        assert task.is_overdue() is False

    def test_is_not_overdue_when_future_due_date(self):
        task = Task("Test task", due_date=datetime.now() + timedelta(days=1))
        assert task.is_overdue() is False

    def test_is_not_overdue_without_due_date(self):
        assert Task("Test task").is_overdue() is False


class TestPriorityComparison:
    @pytest.mark.parametrize("mine,other,expected", [
        (TaskPriority.URGENT, TaskPriority.HIGH, 1),
        (TaskPriority.LOW, TaskPriority.MEDIUM, -1),
        (TaskPriority.MEDIUM, TaskPriority.MEDIUM, 0),
        (TaskPriority.HIGH, TaskPriority.LOW, 1),
    ])
    def test_compare_priority(self, mine, other, expected):
        a = Task("Task A", priority=mine)
        b = Task("Task B", priority=other)
        assert a.compare_priority(b) == expected