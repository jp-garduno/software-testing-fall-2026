from datetime import datetime, timedelta

import pytest
from task import Task, TaskPriority, TaskStatus


@pytest.fixture
def future():
    return datetime.now() + timedelta(days=7)


@pytest.fixture
def task():
    return Task("Test task")


# ---------------- Creación y validación ----------------
class TestTaskCreation:
    def test_task_creation_with_valid_data(self, future):
        t = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, future)
        assert t.title == "Write unit tests"
        assert t.description == "Complete homework 5"
        assert t.status == TaskStatus.TODO
        assert t.priority == TaskPriority.HIGH
        assert t.due_date == future
        assert t.id
        assert t.created_at is not None
        assert t.updated_at is not None

    def test_task_creation_defaults(self):
        t = Task("Default task")
        assert t.priority == TaskPriority.LOW
        assert t.description == ""
        assert t.due_date is None

    def test_task_creation_with_invalid_title_too_short(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_empty_title(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("")

    def test_task_creation_with_invalid_title_too_long(self):
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task("a" * 101)

    def test_task_creation_with_title_boundaries(self):
        assert Task("abc").title == "abc"
        assert len(Task("a" * 100).title) == 100

    def test_task_creation_with_past_due_date(self):
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=datetime.now() - timedelta(days=1))

    def test_task_creation_with_future_due_date(self, future):
        assert Task("Test task", due_date=future).due_date == future

    def test_description_is_truncated_to_500_chars(self):
        assert len(Task("Test task", "x" * 600).description) == 500

    def test_each_task_has_unique_id(self):
        assert Task("Task one").id != Task("Task two").id


# ---------------- Transiciones ----------------
class TestStatusTransitions:
    def test_can_transition_todo_to_in_progress(self, task):
        assert task.can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self, task):
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    def test_cannot_skip_todo_to_done(self, task):
        assert task.can_transition(TaskStatus.DONE) is False

    def test_cannot_transition_done_to_in_progress(self, task):
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False

    @pytest.mark.parametrize(
        "status", [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
    )
    def test_can_transition_any_state_to_archived(self, task, status):
        task.status = status
        assert task.can_transition(TaskStatus.ARCHIVED) is True

    def test_archived_cannot_transition_to_any_state(self, task):
        task.status = TaskStatus.ARCHIVED
        for s in TaskStatus:
            assert task.can_transition(s) is False

    def test_change_status_valid_updates_status_and_timestamp(self, task):
        before = task.updated_at
        task.change_status(TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.updated_at >= before

    def test_change_status_invalid_raises(self, task):
        with pytest.raises(ValueError, match="Invalid transition"):
            task.change_status(TaskStatus.DONE)
        assert task.status == TaskStatus.TODO

    def test_archive_marks_task_as_archived(self, task):
        task.archive()
        assert task.status == TaskStatus.ARCHIVED

    def test_archive_twice_raises(self, task):
        task.archive()
        with pytest.raises(ValueError, match="Invalid transition"):
            task.archive()


# ---------------- Actualización ----------------
class TestTaskUpdate:
    def test_update_all_fields(self, task, future):
        task.update("New title", "New desc", TaskPriority.URGENT, future)
        assert task.title == "New title"
        assert task.description == "New desc"
        assert task.priority == TaskPriority.URGENT
        assert task.due_date == future

    def test_update_with_no_args_keeps_values(self, task):
        task.update()
        assert task.title == "Test task"

    def test_update_invalid_title_raises(self, task):
        with pytest.raises(ValueError, match="at least 3 characters"):
            task.update(title="ab")
        assert task.title == "Test task"

    def test_update_past_due_date_raises(self, task):
        with pytest.raises(ValueError, match="must be in the future"):
            task.update(due_date=datetime.now() - timedelta(days=1))

    def test_update_truncates_long_description(self, task):
        task.update(description="y" * 700)
        assert len(task.description) == 500

    def test_update_archived_task_raises(self, task):
        task.archive()
        with pytest.raises(ValueError, match="archived"):
            task.update(title="Another title")


# ---------------- Vencimiento ----------------
class TestOverdueDetection:
    def test_is_overdue_when_past_due_and_not_done(self, task):
        task.due_date = datetime.now() - timedelta(days=1)
        assert task.is_overdue() is True

    def test_is_not_overdue_when_past_due_but_done(self, task):
        task.due_date = datetime.now() - timedelta(days=1)
        task.status = TaskStatus.DONE
        assert task.is_overdue() is False

    def test_is_not_overdue_when_past_due_but_archived(self, task):
        task.due_date = datetime.now() - timedelta(days=1)
        task.status = TaskStatus.ARCHIVED
        assert task.is_overdue() is False

    def test_is_not_overdue_when_future_due_date(self, future):
        assert Task("Test task", due_date=future).is_overdue() is False

    def test_is_not_overdue_without_due_date(self, task):
        assert task.is_overdue() is False


# ---------------- Prioridad ----------------
class TestPriorityComparison:
    def test_priority_comparison_urgent_higher_than_high(self):
        a = Task("Task A", priority=TaskPriority.URGENT)
        b = Task("Task B", priority=TaskPriority.HIGH)
        assert a.compare_priority(b) == 1

    def test_priority_comparison_low_lower_than_medium(self):
        a = Task("Task A", priority=TaskPriority.LOW)
        b = Task("Task B", priority=TaskPriority.MEDIUM)
        assert a.compare_priority(b) == -1

    def test_priority_comparison_equal(self):
        a = Task("Task A", priority=TaskPriority.HIGH)
        b = Task("Task B", priority=TaskPriority.HIGH)
        assert a.compare_priority(b) == 0
