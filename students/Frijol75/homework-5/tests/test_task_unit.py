"""Unit tests for the Task model (Part 1)."""

from datetime import datetime, timedelta
import pytest
from task import Task, TaskPriority, TaskStatus


class TestTaskCreation:
    """Tests covering task instantiation and initial state."""

    def test_task_creation_with_valid_data(self):
        """Create task with valid title, description, priority and due date."""
        due_date = datetime.now() + timedelta(days=7)
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == due_date
        assert task.id is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_creation_with_defaults(self):
        """Create task using default priority and empty description."""
        task = Task("Default Task")
        assert task.title == "Default Task"
        assert task.description == ""
        assert task.priority == TaskPriority.LOW
        assert task.due_date is None
        assert task.status == TaskStatus.TODO

    def test_task_creation_with_explicit_id(self):
        """Create task with explicit identifier."""
        task = Task("Task with ID", task_id=42)
        assert task.id == 42


class TestTaskValidation:
    """Tests for input validation logic."""

    def test_task_creation_with_invalid_title_too_short(self):
        """Reject title with fewer than 3 characters."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_invalid_title_too_long(self):
        """Reject title exceeding 100 characters."""
        long_title = "a" * 101
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task(long_title)

    def test_task_creation_with_empty_or_none_title(self):
        """Reject empty or None titles."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("")
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(None)

    def test_task_creation_with_non_string_title(self):
        """Reject non-string title types."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task(12345)

    def test_task_creation_with_boundary_title_lengths(self):
        """Accept titles at exactly 3 and 100 characters."""
        t3 = Task("abc")
        assert t3.title == "abc"
        t100 = Task("a" * 100)
        assert len(t100.title) == 100

    def test_task_creation_with_past_due_date(self):
        """Reject due date that is in the past."""
        past_date = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=past_date)

    def test_task_creation_with_invalid_due_date_type(self):
        """Reject non-datetime object for due date."""
        with pytest.raises(TypeError, match="must be a datetime"):
            Task("Test task", due_date="tomorrow")

    def test_task_description_truncation_at_500_chars(self):
        """Ensure description is capped at 500 characters."""
        long_desc = "x" * 600
        task = Task("Long Description Task", description=long_desc)
        assert len(task.description) == 500


class TestStatusTransitions:
    """Tests for lifecycle state transition rules."""

    def test_can_transition_todo_to_in_progress(self):
        """Allow transition from TODO to IN_PROGRESS."""
        task = Task("Test task")
        assert task.can_transition(TaskStatus.IN_PROGRESS) is True

    def test_can_transition_in_progress_to_done(self):
        """Allow transition from IN_PROGRESS to DONE."""
        task = Task("Test task")
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_transition(TaskStatus.DONE) is True

    def test_cannot_transition_done_to_in_progress(self):
        """Reject backward transition from DONE to IN_PROGRESS."""
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False

    def test_cannot_transition_todo_to_done_directly(self):
        """Reject skipping IN_PROGRESS step."""
        task = Task("Test task")
        assert task.can_transition(TaskStatus.DONE) is False

    def test_can_transition_any_active_state_to_archived(self):
        """Allow transition to ARCHIVED from TODO, IN_PROGRESS, or DONE."""
        for initial_status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]:
            task = Task("Test task")
            task.status = initial_status
            assert task.can_transition(TaskStatus.ARCHIVED) is True

    def test_archived_cannot_transition_to_any_state(self):
        """ARCHIVED is a terminal state that rejects any transition."""
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(TaskStatus.TODO) is False
        assert task.can_transition(TaskStatus.IN_PROGRESS) is False
        assert task.can_transition(TaskStatus.DONE) is False
        assert task.can_transition(TaskStatus.ARCHIVED) is False

    def test_transition_to_executes_successfully(self):
        """transition_to updates the status and updated_at timestamp."""
        task = Task("Test task")
        original_time = task.updated_at
        success = task.transition_to(TaskStatus.IN_PROGRESS)
        assert success is True
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.updated_at >= original_time

    def test_transition_to_invalid_raises_value_error(self):
        """transition_to raises ValueError when transition is invalid."""
        task = Task("Test task")
        with pytest.raises(ValueError, match="Invalid transition"):
            task.transition_to(TaskStatus.DONE)


class TestOverdueDetection:
    """Tests for overdue detection logic."""

    def test_is_overdue_when_past_due_and_not_done(self):
        """Task is overdue if past due date and in TODO or IN_PROGRESS."""
        past_date = datetime.now() - timedelta(days=1)
        task = Task("Test task")
        task.due_date = past_date
        assert task.is_overdue() is True

        task.status = TaskStatus.IN_PROGRESS
        assert task.is_overdue() is True

    def test_is_not_overdue_when_past_due_but_done(self):
        """Completed tasks are never overdue."""
        past_date = datetime.now() - timedelta(days=1)
        task = Task("Test task")
        task.due_date = past_date
        task.status = TaskStatus.DONE
        assert task.is_overdue() is False

    def test_is_not_overdue_when_past_due_but_archived(self):
        """Archived tasks are never overdue."""
        past_date = datetime.now() - timedelta(days=1)
        task = Task("Test task")
        task.due_date = past_date
        task.status = TaskStatus.ARCHIVED
        assert task.is_overdue() is False

    def test_is_not_overdue_when_future_due_date(self):
        """Tasks with future due dates are not overdue."""
        task = Task("Test task", due_date=datetime.now() + timedelta(days=2))
        assert task.is_overdue() is False

    def test_is_not_overdue_when_no_due_date(self):
        """Tasks without due dates are not overdue."""
        task = Task("Test task")
        assert task.is_overdue() is False


class TestPriorityComparison:
    """Tests for comparing priorities between tasks."""

    def test_priority_comparison_urgent_higher_than_high(self):
        """URGENT is higher priority than HIGH."""
        t_urgent = Task("Urgent Task", priority=TaskPriority.URGENT)
        t_high = Task("High Task", priority=TaskPriority.HIGH)
        assert t_urgent.compare_priority(t_high) == 1
        assert t_high.compare_priority(t_urgent) == -1

    def test_priority_comparison_low_lower_than_medium(self):
        """LOW is lower priority than MEDIUM."""
        t_low = Task("Low Task", priority=TaskPriority.LOW)
        t_med = Task("Med Task", priority=TaskPriority.MEDIUM)
        assert t_low.compare_priority(t_med) == -1
        assert t_med.compare_priority(t_low) == 1

    def test_priority_comparison_equal_priorities(self):
        """Tasks with identical priorities compare as equal (0)."""
        t1 = Task("Task 1", priority=TaskPriority.HIGH)
        t2 = Task("Task 2", priority=TaskPriority.HIGH)
        assert t1.compare_priority(t2) == 0


class TestTaskUpdateAndSerialization:
    """Tests for updating task attributes and serializing to dictionary."""

    def test_task_update_attributes_success(self):
        """Update title, description, priority, and due date successfully."""
        task = Task("Initial Title")
        new_due = datetime.now() + timedelta(days=5)
        task.update(
            title="Updated Title",
            description="Updated Description",
            priority=TaskPriority.HIGH,
            due_date=new_due,
        )

        assert task.title == "Updated Title"
        assert task.description == "Updated Description"
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == new_due

    def test_task_update_on_archived_task_raises_error(self):
        """Cannot update an archived task."""
        task = Task("Initial Title")
        task.status = TaskStatus.ARCHIVED
        with pytest.raises(ValueError, match="Cannot update archived task"):
            task.update(title="New Title")

    def test_task_to_dict_representation(self):
        """Ensure to_dict returns complete task attributes."""
        due = datetime.now() + timedelta(days=1)
        task = Task("Dict Task", "Description", TaskPriority.MEDIUM, due, task_id=10)
        data = task.to_dict()

        assert data["id"] == 10
        assert data["title"] == "Dict Task"
        assert data["description"] == "Description"
        assert data["status"] == "TODO"
        assert data["priority"] == "MEDIUM"
        assert data["due_date"] == due.isoformat()
        assert "created_at" in data
        assert "updated_at" in data
