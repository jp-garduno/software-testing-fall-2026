import pytest
from datetime import datetime, timedelta
from task import Task, TaskStatus, TaskPriority

class TestTaskCreation:
    def test_task_creation_with_valid_data(self):
        due_date = datetime.now() + timedelta(days=7)
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date)
        assert task.title == "Write unit tests"
        assert task.status == TaskStatus.TODO
        assert task.due_date == due_date

    def test_task_creation_with_invalid_title_too_short(self):
        with pytest.raises(ValueError, match="at least 3 characters"): Task("ab")

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"): Task("a" * 101)

    def test_task_creation_with_past_due_date(self):
        with pytest.raises(ValueError, match="must be in the future"): 
            Task("Test task", due_date=datetime.now() - timedelta(days=1))

class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self):
        assert Task("Test task").can_transition(TaskStatus.IN_PROGRESS) == True

    def test_cannot_transition_done_to_in_progress(self):
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) == False

    def test_can_transition_any_state_to_archived(self):
        assert Task("Test task").can_transition(TaskStatus.ARCHIVED) == True

    def test_archived_cannot_transition_to_any_state(self):
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(TaskStatus.TODO) == False

class TestOverdueDetection:
    def test_is_overdue_when_past_due_and_not_done(self):
        task = Task("Test task")
        task.due_date = datetime.now() - timedelta(days=1)
        assert task.is_overdue() == True

    def test_is_not_overdue_when_past_due_but_done(self):
        task = Task("Test task")
        task.due_date = datetime.now() - timedelta(days=1)
        task.status = TaskStatus.DONE
        assert task.is_overdue() == False

    def test_is_not_overdue_when_future_due_date(self):
        task = Task("Test task", due_date=datetime.now() + timedelta(days=1))
        assert task.is_overdue() == False

class TestPriorityComparison:
    def test_priority_comparison_urgent_higher_than_high(self):
        t1 = Task("T1", priority=TaskPriority.URGENT)
        t2 = Task("T2", priority=TaskPriority.HIGH)
        assert t1.compare_priority(t2) == 1

    def test_priority_comparison_low_lower_than_medium(self):
        t1 = Task("T1", priority=TaskPriority.LOW)
        t2 = Task("T2", priority=TaskPriority.MEDIUM)
        assert t1.compare_priority(t2) == -1