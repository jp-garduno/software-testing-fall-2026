# Homework 5: White Box Testing & Coverage

**Module**: 5 - White Box Testing & Coverage  
**Due Date**: End of Week 8  
**Points**: 110 (100 base + 10 bonus)  
**Estimated Time**: 5-6 hours

---

## 🎯 Objectives

This homework will help you:

- Master unit testing with complete isolation and independence
- Implement integration tests with proper component interaction
- Understand and apply code coverage metrics (statement, branch, function)
- Use mocking and test doubles to isolate external dependencies
- Achieve high coverage through systematic white box techniques
- Analyze coverage gaps and make informed testing decisions
- Balance coverage metrics with meaningful test quality
- Test internal logic, control flow, and data flow paths

---

## 📋 Assignment Overview

You will build and test a **Task Management System** from scratch. This assignment requires both implementation (production code) and comprehensive testing (unit tests, integration tests, mocking) using either Python or JavaScript.

The system includes complex business logic, external dependencies, state management, and validation rules - perfect for applying white box testing techniques and achieving high code coverage.

---

## 📝 System Under Test: TaskFlow - Task Management System

### System Description

TaskFlow is a task management system that helps users organize, prioritize, and track their tasks with notifications and lifecycle management.

### Task Model

Each task has the following attributes:

- **title**: String (3-100 characters, required)
- **description**: String (optional, max 500 characters)
- **status**: Enum (TODO, IN_PROGRESS, DONE, ARCHIVED)
- **priority**: Enum (LOW, MEDIUM, HIGH, URGENT)
- **due_date**: DateTime (must be in the future when created)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-updated)

### Status Transitions

Valid state transitions:

```
TODO → IN_PROGRESS → DONE → ARCHIVED
  ↓         ↓          ↓
ARCHIVED ← ARCHIVED ← ARCHIVED
```

**Rules**:

- Cannot transition backwards (e.g., DONE → IN_PROGRESS is invalid)
- Can always transition to ARCHIVED from any state
- ARCHIVED is a terminal state (no transitions out)

### Priority Levels

- **LOW**: Default priority
- **MEDIUM**: Normal priority
- **HIGH**: Important tasks
- **URGENT**: Critical tasks requiring immediate attention

**Sorting**: URGENT > HIGH > MEDIUM > LOW

### Core Components

1. **Task (Model)**

   - Data structure and validation
   - Status transition logic
   - Overdue detection
   - Priority comparison

2. **TaskRepository (Data Layer)**

   - CRUD operations (Create, Read, Update, Delete)
   - Task searching and filtering
   - Persistence operations (to be mocked)
   - Database error handling

3. **TaskService (Business Logic)**

   - Task creation with validation
   - Task updates and status management
   - Business rule enforcement
   - Orchestrates Repository and NotificationService

4. **NotificationService (External Dependency)**
   - Send email notifications
   - Send SMS notifications
   - Trigger on status changes
   - Trigger on overdue tasks
   - External API calls (to be mocked)

### Business Rules

1. **Task Creation**:

   - Title is required (3-100 characters)
   - Title must be unique (no duplicates)
   - Due date must be in the future
   - Status starts as TODO
   - created_at is automatically set

2. **Task Updates**:

   - Can update title (must remain unique)
   - Can update description
   - Can update priority
   - Can update due_date (must be in future)
   - updated_at is automatically updated

3. **Status Transitions**:

   - Must follow valid transition paths
   - Trigger notification on status change
   - Cannot modify other fields when archiving

4. **Task Deletion**:

   - Soft delete (mark as ARCHIVED)
   - Cannot restore archived tasks
   - Permanently deleted tasks cannot be recovered

5. **Overdue Detection**:

   - Task is overdue if due_date < current_time AND status != DONE
   - Overdue tasks trigger notifications
   - Check for overdue tasks periodically

6. **Search and Filter**:
   - Filter by status
   - Filter by priority
   - Filter by date range
   - Search by title (partial match)
   - Combine multiple filters

---

## 📝 Part 1: Unit Tests (20 points)

Write comprehensive unit tests for individual methods and functions with complete isolation.

### 1.1 Requirements

**Minimum Test Coverage**:

- At least 15 unit tests
- Test ALL methods in Task model
- Test validation logic thoroughly
- Test priority comparisons
- Test overdue detection
- > 90% statement coverage on model classes
- All tests completely isolated (no external dependencies)

### 1.2 What to Test

**Task Model Tests**:

```python
# Python examples
test_task_creation_with_valid_data
test_task_creation_with_invalid_title_too_short
test_task_creation_with_invalid_title_too_long
test_task_creation_with_past_due_date
test_task_creation_with_future_due_date
test_can_transition_todo_to_in_progress
test_can_transition_in_progress_to_done
test_cannot_transition_done_to_in_progress
test_can_transition_any_state_to_archived
test_archived_cannot_transition_to_any_state
test_is_overdue_when_past_due_and_not_done
test_is_not_overdue_when_past_due_but_done
test_is_not_overdue_when_future_due_date
test_priority_comparison_urgent_higher_than_high
test_priority_comparison_low_lower_than_medium
```

### 1.3 Example Test Structure

**Python Example**:

```python
# task.py

from datetime import datetime, timedelta
from enum import Enum

class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class Task:
    def __init__(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        self.validate_title(title)
        self.title = title
        self.description = description[:500] if description else ""
        self.status = TaskStatus.TODO
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if due_date:
            self.validate_due_date(due_date)

    @staticmethod
    def validate_title(title):
        if not title or len(title) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    def validate_due_date(self, due_date):
        if due_date < datetime.now():
            raise ValueError("Due date must be in the future")

    def can_transition(self, new_status):
        """Check if transition to new_status is valid"""
        if self.status == TaskStatus.ARCHIVED:
            return False

        if new_status == TaskStatus.ARCHIVED:
            return True

        transitions = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
            TaskStatus.DONE: []
        }

        return new_status in transitions.get(self.status, [])

    def is_overdue(self):
        """Check if task is overdue"""
        if self.status == TaskStatus.DONE or self.status == TaskStatus.ARCHIVED:
            return False
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    def compare_priority(self, other_task):
        """Compare priority with another task. Returns 1 if higher, -1 if lower, 0 if equal"""
        if self.priority.value > other_task.priority.value:
            return 1
        elif self.priority.value < other_task.priority.value:
            return -1
        return 0

# test_task_unit.py

import pytest
from datetime import datetime, timedelta
from task import Task, TaskStatus, TaskPriority

class TestTaskCreation:

    def test_task_creation_with_valid_data(self):
        """Unit test: Create task with valid title and due date"""
        due_date = datetime.now() + timedelta(days=7)
        task = Task("Write unit tests", "Complete homework 5", TaskPriority.HIGH, due_date)

        assert task.title == "Write unit tests"
        assert task.description == "Complete homework 5"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == due_date

    def test_task_creation_with_invalid_title_too_short(self):
        """Unit test: Reject title with fewer than 3 characters"""
        with pytest.raises(ValueError, match="at least 3 characters"):
            Task("ab")

    def test_task_creation_with_invalid_title_too_long(self):
        """Unit test: Reject title exceeding 100 characters"""
        long_title = "a" * 101
        with pytest.raises(ValueError, match="not exceed 100 characters"):
            Task(long_title)

    def test_task_creation_with_past_due_date(self):
        """Unit test: Reject past due date"""
        past_date = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError, match="must be in the future"):
            Task("Test task", due_date=past_date)

class TestStatusTransitions:

    def test_can_transition_todo_to_in_progress(self):
        """Unit test: Valid transition from TODO to IN_PROGRESS"""
        task = Task("Test task")
        assert task.can_transition(TaskStatus.IN_PROGRESS) == True

    def test_cannot_transition_done_to_in_progress(self):
        """Unit test: Invalid backward transition"""
        task = Task("Test task")
        task.status = TaskStatus.DONE
        assert task.can_transition(TaskStatus.IN_PROGRESS) == False

    def test_archived_cannot_transition_to_any_state(self):
        """Unit test: ARCHIVED is terminal state"""
        task = Task("Test task")
        task.status = TaskStatus.ARCHIVED
        assert task.can_transition(TaskStatus.TODO) == False
        assert task.can_transition(TaskStatus.IN_PROGRESS) == False
        assert task.can_transition(TaskStatus.DONE) == False

class TestOverdueDetection:

    def test_is_overdue_when_past_due_and_not_done(self):
        """Unit test: Task is overdue if past due date and not completed"""
        past_date = datetime.now() - timedelta(days=1)
        task = Task("Test task", due_date=past_date)
        task.due_date = past_date  # Set after creation to bypass validation
        assert task.is_overdue() == True

    def test_is_not_overdue_when_past_due_but_done(self):
        """Unit test: Completed tasks are never overdue"""
        past_date = datetime.now() - timedelta(days=1)
        task = Task("Test task")
        task.due_date = past_date
        task.status = TaskStatus.DONE
        assert task.is_overdue() == False
```

**JavaScript Example**:

```javascript
// task.js

const TaskStatus = {
  TODO: "TODO",
  IN_PROGRESS: "IN_PROGRESS",
  DONE: "DONE",
  ARCHIVED: "ARCHIVED",
};

const TaskPriority = {
  LOW: 1,
  MEDIUM: 2,
  HIGH: 3,
  URGENT: 4,
};

class Task {
  constructor(
    title,
    description = "",
    priority = TaskPriority.LOW,
    dueDate = null,
  ) {
    Task.validateTitle(title);
    this.title = title;
    this.description = description.substring(0, 500);
    this.status = TaskStatus.TODO;
    this.priority = priority;
    this.dueDate = dueDate;
    this.createdAt = new Date();
    this.updatedAt = new Date();

    if (dueDate) {
      this.validateDueDate(dueDate);
    }
  }

  static validateTitle(title) {
    if (!title || title.length < 3) {
      throw new Error("Title must be at least 3 characters");
    }
    if (title.length > 100) {
      throw new Error("Title must not exceed 100 characters");
    }
  }

  validateDueDate(dueDate) {
    if (dueDate < new Date()) {
      throw new Error("Due date must be in the future");
    }
  }

  canTransition(newStatus) {
    if (this.status === TaskStatus.ARCHIVED) {
      return false;
    }

    if (newStatus === TaskStatus.ARCHIVED) {
      return true;
    }

    const transitions = {
      [TaskStatus.TODO]: [TaskStatus.IN_PROGRESS],
      [TaskStatus.IN_PROGRESS]: [TaskStatus.DONE],
      [TaskStatus.DONE]: [],
    };

    return (transitions[this.status] || []).includes(newStatus);
  }

  isOverdue() {
    if (
      this.status === TaskStatus.DONE ||
      this.status === TaskStatus.ARCHIVED
    ) {
      return false;
    }
    if (!this.dueDate) {
      return false;
    }
    return new Date() > this.dueDate;
  }

  comparePriority(otherTask) {
    if (this.priority > otherTask.priority) return 1;
    if (this.priority < otherTask.priority) return -1;
    return 0;
  }
}

module.exports = { Task, TaskStatus, TaskPriority };

// task.test.js

const { Task, TaskStatus, TaskPriority } = require("./task");

describe("Task Creation", () => {
  test("Unit test: Create task with valid data", () => {
    const dueDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    const task = new Task(
      "Write unit tests",
      "Complete homework 5",
      TaskPriority.HIGH,
      dueDate,
    );

    expect(task.title).toBe("Write unit tests");
    expect(task.description).toBe("Complete homework 5");
    expect(task.status).toBe(TaskStatus.TODO);
    expect(task.priority).toBe(TaskPriority.HIGH);
    expect(task.dueDate).toBe(dueDate);
  });

  test("Unit test: Reject title with fewer than 3 characters", () => {
    expect(() => new Task("ab")).toThrow("at least 3 characters");
  });

  test("Unit test: Reject title exceeding 100 characters", () => {
    const longTitle = "a".repeat(101);
    expect(() => new Task(longTitle)).toThrow("not exceed 100 characters");
  });
});

describe("Status Transitions", () => {
  test("Unit test: Valid transition from TODO to IN_PROGRESS", () => {
    const task = new Task("Test task");
    expect(task.canTransition(TaskStatus.IN_PROGRESS)).toBe(true);
  });

  test("Unit test: Invalid backward transition", () => {
    const task = new Task("Test task");
    task.status = TaskStatus.DONE;
    expect(task.canTransition(TaskStatus.IN_PROGRESS)).toBe(false);
  });
});
```

### 1.4 Grading Criteria (20 points)

- **Test Coverage** (8 pts): At least 15 tests, >90% statement coverage on models
- **Test Quality** (7 pts): Clear names, proper assertions, good test data
- **Isolation** (5 pts): No external dependencies, tests run independently

---

## 📝 Part 2: Integration Tests (25 points)

Write integration tests that verify multiple components working together with proper mocking.

### 2.1 Requirements

**Minimum Test Coverage**:

- At least 10 integration tests
- Test TaskService with TaskRepository
- Test complete workflows (create → update → complete)
- Test business rule enforcement across components
- Mock NotificationService (external dependency)
- Mock TaskRepository (database operations)
- > 85% branch coverage overall
- All tests pass and are meaningful

### 2.2 What to Test

**Integration Test Scenarios**:

```
test_create_task_success_with_notification
test_create_task_with_duplicate_title_fails
test_update_task_status_triggers_notification
test_complete_workflow_todo_to_done
test_archive_task_prevents_further_updates
test_overdue_task_detection_triggers_notification
test_search_tasks_by_status
test_filter_tasks_by_priority
test_update_task_with_invalid_transition_fails
test_delete_task_marks_as_archived
test_repository_failure_handled_gracefully
test_notification_failure_does_not_break_workflow
```

### 2.3 Example Integration Test Structure

**Python Example**:

```python
# task_repository.py

class TaskRepository:
    """Data access layer for tasks (to be mocked in tests)"""

    def __init__(self, database):
        self.database = database

    def save(self, task):
        """Save task to database"""
        # In real implementation, this would interact with database
        raise NotImplementedError("Must be mocked in tests")

    def find_by_id(self, task_id):
        """Find task by ID"""
        raise NotImplementedError("Must be mocked in tests")

    def find_by_title(self, title):
        """Find task by exact title"""
        raise NotImplementedError("Must be mocked in tests")

    def find_all(self):
        """Get all tasks"""
        raise NotImplementedError("Must be mocked in tests")

    def delete(self, task_id):
        """Delete task"""
        raise NotImplementedError("Must be mocked in tests")

# notification_service.py

class NotificationService:
    """External notification service (to be mocked in tests)"""

    def send_email(self, recipient, subject, body):
        """Send email notification"""
        raise NotImplementedError("Must be mocked in tests")

    def send_sms(self, phone_number, message):
        """Send SMS notification"""
        raise NotImplementedError("Must be mocked in tests")

# task_service.py

class TaskService:
    """Business logic layer for task management"""

    def __init__(self, repository, notification_service):
        self.repository = repository
        self.notification_service = notification_service

    def create_task(self, title, description="", priority=TaskPriority.LOW, due_date=None):
        """Create a new task with validation"""
        # Check for duplicate title
        existing = self.repository.find_by_title(title)
        if existing:
            raise ValueError(f"Task with title '{title}' already exists")

        # Create task
        task = Task(title, description, priority, due_date)

        # Save to repository
        self.repository.save(task)

        # Send notification
        self.notification_service.send_email(
            "user@example.com",
            "New Task Created",
            f"Task '{title}' has been created"
        )

        return task

    def update_task_status(self, task_id, new_status):
        """Update task status with validation and notification"""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if not task.can_transition(new_status):
            raise ValueError(f"Invalid transition from {task.status} to {new_status}")

        old_status = task.status
        task.status = new_status
        task.updated_at = datetime.now()

        self.repository.save(task)

        # Notify on status change
        self.notification_service.send_email(
            "user@example.com",
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status} to {new_status}"
        )

        return task

    def check_overdue_tasks(self):
        """Check for overdue tasks and send notifications"""
        all_tasks = self.repository.find_all()
        overdue_tasks = [task for task in all_tasks if task.is_overdue()]

        for task in overdue_tasks:
            self.notification_service.send_email(
                "user@example.com",
                "Task Overdue",
                f"Task '{task.title}' is overdue!"
            )

        return overdue_tasks

# test_task_integration.py

import pytest
from unittest.mock import Mock, MagicMock, call
from datetime import datetime, timedelta
from task import Task, TaskStatus, TaskPriority
from task_repository import TaskRepository
from notification_service import NotificationService
from task_service import TaskService

class TestTaskServiceIntegration:

    @pytest.fixture
    def mock_repository(self):
        """Create mock repository"""
        return Mock(spec=TaskRepository)

    @pytest.fixture
    def mock_notification_service(self):
        """Create mock notification service"""
        return Mock(spec=NotificationService)

    @pytest.fixture
    def task_service(self, mock_repository, mock_notification_service):
        """Create TaskService with mocked dependencies"""
        return TaskService(mock_repository, mock_notification_service)

    def test_create_task_success_with_notification(self, task_service, mock_repository, mock_notification_service):
        """Integration: Creating task saves to repository and sends notification"""
        # Arrange
        mock_repository.find_by_title.return_value = None

        # Act
        task = task_service.create_task("Write tests", "Unit and integration tests", TaskPriority.HIGH)

        # Assert
        assert task.title == "Write tests"
        mock_repository.save.assert_called_once_with(task)
        mock_notification_service.send_email.assert_called_once()
        assert "New Task Created" in mock_notification_service.send_email.call_args[0][1]

    def test_create_task_with_duplicate_title_fails(self, task_service, mock_repository, mock_notification_service):
        """Integration: Cannot create task with duplicate title"""
        # Arrange
        existing_task = Task("Existing Task")
        mock_repository.find_by_title.return_value = existing_task

        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            task_service.create_task("Existing Task")

        # Verify no save or notification occurred
        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_update_task_status_triggers_notification(self, task_service, mock_repository, mock_notification_service):
        """Integration: Status update saves and notifies"""
        # Arrange
        task = Task("Test Task")
        task.status = TaskStatus.TODO
        mock_repository.find_by_id.return_value = task

        # Act
        updated_task = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        # Assert
        assert updated_task.status == TaskStatus.IN_PROGRESS
        mock_repository.save.assert_called_once()
        mock_notification_service.send_email.assert_called_once()
        call_args = mock_notification_service.send_email.call_args[0]
        assert "Status Updated" in call_args[1]
        assert "TODO" in call_args[2]
        assert "IN_PROGRESS" in call_args[2]

    def test_complete_workflow_todo_to_done(self, task_service, mock_repository, mock_notification_service):
        """Integration: Complete workflow through multiple status changes"""
        # Arrange
        task = Task("Complete workflow task")
        mock_repository.find_by_id.return_value = task

        # Act & Assert - TODO to IN_PROGRESS
        task = task_service.update_task_status(1, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS

        # IN_PROGRESS to DONE
        task = task_service.update_task_status(1, TaskStatus.DONE)
        assert task.status == TaskStatus.DONE

        # Verify save called twice and two notifications sent
        assert mock_repository.save.call_count == 2
        assert mock_notification_service.send_email.call_count == 2

    def test_update_task_with_invalid_transition_fails(self, task_service, mock_repository, mock_notification_service):
        """Integration: Invalid status transition is rejected"""
        # Arrange
        task = Task("Test Task")
        task.status = TaskStatus.DONE
        mock_repository.find_by_id.return_value = task

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid transition"):
            task_service.update_task_status(1, TaskStatus.IN_PROGRESS)

        # Task not saved, no notification
        mock_repository.save.assert_not_called()
        mock_notification_service.send_email.assert_not_called()

    def test_check_overdue_tasks_triggers_notifications(self, task_service, mock_repository, mock_notification_service):
        """Integration: Overdue check finds tasks and sends notifications"""
        # Arrange
        overdue_task = Task("Overdue task")
        overdue_task.due_date = datetime.now() - timedelta(days=1)

        not_overdue_task = Task("Future task")
        not_overdue_task.due_date = datetime.now() + timedelta(days=1)

        mock_repository.find_all.return_value = [overdue_task, not_overdue_task]

        # Act
        overdue_tasks = task_service.check_overdue_tasks()

        # Assert
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].title == "Overdue task"
        mock_notification_service.send_email.assert_called_once()
        assert "overdue" in mock_notification_service.send_email.call_args[0][2].lower()
```

**JavaScript Example**:

```javascript
// taskService.js

class TaskService {
  constructor(repository, notificationService) {
    this.repository = repository;
    this.notificationService = notificationService;
  }

  async createTask(
    title,
    description = "",
    priority = TaskPriority.LOW,
    dueDate = null,
  ) {
    const existing = await this.repository.findByTitle(title);
    if (existing) {
      throw new Error(`Task with title '${title}' already exists`);
    }

    const task = new Task(title, description, priority, dueDate);
    await this.repository.save(task);

    await this.notificationService.sendEmail(
      "user@example.com",
      "New Task Created",
      `Task '${title}' has been created`,
    );

    return task;
  }

  async updateTaskStatus(taskId, newStatus) {
    const task = await this.repository.findById(taskId);
    if (!task) {
      throw new Error(`Task ${taskId} not found`);
    }

    if (!task.canTransition(newStatus)) {
      throw new Error(`Invalid transition from ${task.status} to ${newStatus}`);
    }

    const oldStatus = task.status;
    task.status = newStatus;
    task.updatedAt = new Date();

    await this.repository.save(task);

    await this.notificationService.sendEmail(
      "user@example.com",
      "Task Status Updated",
      `Task '${task.title}' changed from ${oldStatus} to ${newStatus}`,
    );

    return task;
  }
}

// taskService.test.js

const { Task, TaskStatus, TaskPriority } = require("./task");
const { TaskService } = require("./taskService");

describe("TaskService Integration Tests", () => {
  let mockRepository;
  let mockNotificationService;
  let taskService;

  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
      findByTitle: jest.fn(),
      findAll: jest.fn(),
    };

    mockNotificationService = {
      sendEmail: jest.fn(),
      sendSms: jest.fn(),
    };

    taskService = new TaskService(mockRepository, mockNotificationService);
  });

  test("Integration: Creating task saves to repository and sends notification", async () => {
    mockRepository.findByTitle.mockResolvedValue(null);

    const task = await taskService.createTask(
      "Write tests",
      "Unit and integration tests",
      TaskPriority.HIGH,
    );

    expect(task.title).toBe("Write tests");
    expect(mockRepository.save).toHaveBeenCalledWith(task);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail.mock.calls[0][1]).toContain(
      "New Task Created",
    );
  });

  test("Integration: Cannot create task with duplicate title", async () => {
    const existingTask = new Task("Existing Task");
    mockRepository.findByTitle.mockResolvedValue(existingTask);

    await expect(taskService.createTask("Existing Task")).rejects.toThrow(
      "already exists",
    );

    expect(mockRepository.save).not.toHaveBeenCalled();
    expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
  });

  test("Integration: Status update saves and notifies", async () => {
    const task = new Task("Test Task");
    task.status = TaskStatus.TODO;
    mockRepository.findById.mockResolvedValue(task);

    const updatedTask = await taskService.updateTaskStatus(
      1,
      TaskStatus.IN_PROGRESS,
    );

    expect(updatedTask.status).toBe(TaskStatus.IN_PROGRESS);
    expect(mockRepository.save).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail.mock.calls[0][2]).toContain(
      "TODO",
    );
    expect(mockNotificationService.sendEmail.mock.calls[0][2]).toContain(
      "IN_PROGRESS",
    );
  });
});
```

### 2.4 Grading Criteria (25 points)

- **Test Coverage** (10 pts): At least 10 tests, complete workflows, >85% branch coverage
- **Mocking Quality** (8 pts): Proper use of mocks, verify interactions, test isolation
- **Business Logic** (7 pts): Test business rules, error scenarios, edge cases

---

## 📝 Part 3: Coverage Analysis (25 points)

Generate and analyze code coverage reports to achieve comprehensive testing.

### 3.1 Requirements

**Coverage Goals**:

- > 85% statement coverage overall
- > 80% branch coverage overall
- > 90% function coverage
- Generate HTML coverage reports
- Document untested code paths
- Justify why certain paths aren't tested (if any)

### 3.2 Generating Coverage Reports

**Python with pytest-cov**:

```bash
# Install coverage tools
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

**JavaScript with Jest**:

```bash
# Jest has built-in coverage
npm test -- --coverage --coverageDirectory=coverage

# View HTML report
open coverage/index.html
```

### 3.3 Coverage Report Requirements

Create a document (`coverage-analysis.md`) with:

**1. Coverage Summary Table**:

```markdown
## Coverage Summary

| Metric             | Threshold | Achieved | Status  |
| ------------------ | --------- | -------- | ------- |
| Statement Coverage | 85%       | 91%      | ✅ Pass |
| Branch Coverage    | 80%       | 84%      | ✅ Pass |
| Function Coverage  | 90%       | 95%      | ✅ Pass |
| Line Coverage      | 85%       | 90%      | ✅ Pass |

## Coverage by File

| File                    | Statements | Branches | Functions | Lines |
| ----------------------- | ---------- | -------- | --------- | ----- |
| task.py                 | 98%        | 95%      | 100%      | 97%   |
| task_service.py         | 92%        | 85%      | 95%       | 91%   |
| task_repository.py      | 85%        | 78%      | 90%       | 84%   |
| notification_service.py | 88%        | 80%      | 100%      | 87%   |
```

**2. Untested Code Paths**:

Document any code not covered and explain why:

````markdown
## Untested Code Paths

### task_service.py - Lines 145-150

**Code**:

```python
except DatabaseConnectionError as e:
    logger.error(f"Database connection failed: {e}")
    raise SystemError("Service temporarily unavailable")
```
````

**Reason**: This is infrastructure error handling for database connection failures. Testing this would require simulating database infrastructure failures, which is beyond the scope of unit/integration tests. This would be tested in system/end-to-end tests with actual database infrastructure.

**Risk**: Low - Standard error handling pattern

### notification_service.py - Line 67

**Code**:

```python
if retry_count > MAX_RETRIES:
    logger.warning("Max retries exceeded")
```

**Reason**: Edge case for notification retry logic. Would require complex mocking of time-based retry mechanisms. The retry logic itself is tested; this specific warning log is not covered.

**Risk**: Very Low - Logging only, no functional impact

````

**3. Screenshots**:

Include:
- Terminal output showing coverage percentages
- HTML coverage report highlighting covered/uncovered lines
- Coverage trends (if running tests multiple times)

**4. Coverage Improvement Strategy**:

```markdown
## How Coverage Goals Were Achieved

### Initial Coverage: 72%

Initial test run showed gaps in:
- Error handling paths (15% uncovered)
- Edge cases in validation (8% uncovered)
- Some utility methods (5% uncovered)

### Strategy Applied

1. **Added boundary value tests** for all validation methods
   - Improved validation coverage from 78% to 98%

2. **Added negative test cases** for all business rules
   - Improved error handling coverage from 65% to 88%

3. **Added state transition tests** for all possible transitions
   - Improved state management coverage from 70% to 95%

4. **Mocked external dependencies** to test all code paths
   - Improved integration test coverage from 68% to 92%

### Final Coverage: 91%

Systematic addition of 12 additional tests targeting specific uncovered branches.
````

### 3.4 Grading Criteria (25 points)

- **Coverage Metrics** (10 pts): Achieve >85% statement, >80% branch coverage
- **Reports** (8 pts): Complete HTML reports, clear screenshots, well-documented
- **Analysis** (7 pts): Identify gaps, justify untested paths, improvement strategy

---

## 📝 Part 4: Mocking & Test Isolation (20 points)

Demonstrate proper use of test doubles to isolate components and test various scenarios.

### 4.1 Requirements

**Mocking Goals**:

- Mock TaskRepository for all database operations
- Mock NotificationService for all external API calls
- Test error scenarios (database failures, notification failures)
- Use appropriate test doubles (mocks vs stubs vs fakes)
- Verify mock interactions
- Tests run fast (<1 second for full suite)

### 4.2 Types of Test Doubles

**Mock**: Verify behavior (method calls, arguments)

```python
mock_repository.save.assert_called_once_with(task)
mock_notification.send_email.assert_called_with("user@example.com", "Subject", "Body")
```

**Stub**: Return predefined responses

```python
mock_repository.find_by_title.return_value = None  # Not found
mock_repository.find_by_id.return_value = task  # Found
```

**Fake**: Simplified working implementation

```python
class FakeTaskRepository:
    def __init__(self):
        self.tasks = {}

    def save(self, task):
        self.tasks[task.id] = task

    def find_by_id(self, task_id):
        return self.tasks.get(task_id)
```

### 4.3 Testing Error Scenarios

**Python Example**:

```python
def test_repository_failure_handled_gracefully(self, task_service, mock_repository, mock_notification_service):
    """Integration: Handle repository failure gracefully"""
    # Arrange
    mock_repository.find_by_title.return_value = None
    mock_repository.save.side_effect = Exception("Database connection failed")

    # Act & Assert
    with pytest.raises(Exception, match="Database connection failed"):
        task_service.create_task("Test Task")

    # Notification should not be sent if save fails
    mock_notification_service.send_email.assert_not_called()

def test_notification_failure_does_not_break_workflow(self, task_service, mock_repository, mock_notification_service):
    """Integration: Notification failure should not prevent task creation"""
    # Arrange
    mock_repository.find_by_title.return_value = None
    mock_notification_service.send_email.side_effect = Exception("SMTP server unavailable")

    # Act - should succeed despite notification failure
    task = task_service.create_task("Test Task")

    # Assert
    assert task.title == "Test Task"
    mock_repository.save.assert_called_once()
    # Notification was attempted but failed
    mock_notification_service.send_email.assert_called_once()

def test_multiple_notification_channels(self, task_service, mock_repository, mock_notification_service):
    """Integration: Test multiple notification methods"""
    # Arrange
    mock_repository.find_by_title.return_value = None

    # Act
    task = task_service.create_task_with_sms("Urgent Task", priority=TaskPriority.URGENT)

    # Assert - verify both email and SMS sent for urgent tasks
    assert mock_notification_service.send_email.called
    assert mock_notification_service.send_sms.called
```

**JavaScript Example**:

```javascript
test("Integration: Handle repository failure gracefully", async () => {
  mockRepository.findByTitle.mockResolvedValue(null);
  mockRepository.save.mockRejectedValue(
    new Error("Database connection failed"),
  );

  await expect(taskService.createTask("Test Task")).rejects.toThrow(
    "Database connection failed",
  );

  expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
});

test("Integration: Notification failure should not prevent task creation", async () => {
  mockRepository.findByTitle.mockResolvedValue(null);
  mockNotificationService.sendEmail.mockRejectedValue(
    new Error("SMTP server unavailable"),
  );

  const task = await taskService.createTask("Test Task");

  expect(task.title).toBe("Test Task");
  expect(mockRepository.save).toHaveBeenCalledTimes(1);
  expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
});
```

### 4.4 Verifying Mock Interactions

**Verify call count**:

```python
mock_repository.save.assert_called_once()
assert mock_notification.send_email.call_count == 3
```

**Verify call arguments**:

```python
mock_repository.save.assert_called_with(task)
mock_notification.send_email.assert_called_with("user@example.com", "Subject", ANY)
```

**Verify call order**:

```python
mock_repository.save.assert_called()
mock_notification.send_email.assert_called()
# Verify save happened before notification
assert mock_repository.save.call_args < mock_notification.send_email.call_args
```

### 4.5 Grading Criteria (20 points)

- **Mock Usage** (8 pts): Proper mocking of all external dependencies
- **Test Isolation** (6 pts): Tests completely isolated, run fast, no side effects
- **Error Scenarios** (6 pts): Test failure cases, verify error handling

---

## 📝 Part 5: Analysis Report (10 points)

Write a comprehensive analysis report (400-600 words) reflecting on your experience with white box testing and coverage.

### 5.1 Required Sections

**1. Coverage Metrics Achievement** (2 points)

- How did you achieve the coverage goals?
- What strategies were most effective?
- Which code was hardest to cover and why?

**2. Challenges in Reaching Coverage Goals** (2 points)

- What obstacles did you encounter?
- How did you overcome them?
- Were there diminishing returns at high coverage percentages?

**3. Benefits of Mocking External Dependencies** (2 points)

- How did mocking improve your tests?
- What would be different without mocking?
- Did mocking make tests easier or harder to write?

**4. Trade-offs Between Coverage and Test Quality** (2 points)

- Is 100% coverage worth pursuing?
- Did you write any "bad tests" just to increase coverage?
- How do you balance coverage metrics with meaningful tests?

**5. Lessons Learned About White Box Testing** (2 points)

- What surprised you?
- What would you do differently next time?
- How will you apply this in future projects?

### 5.2 Example Report Structure

```markdown
# White Box Testing & Coverage Analysis Report

## Executive Summary

This report reflects on the experience of achieving high code coverage through systematic white box testing of the TaskFlow task management system. Key findings include...

## Coverage Metrics Achievement

To achieve the target of >85% statement coverage and >80% branch coverage, I employed a systematic approach:

First, I wrote comprehensive unit tests covering all public methods in the Task model. This immediately achieved 92% coverage on the model itself. Next, I focused on branch coverage by identifying all conditional statements (if/else, switch cases) and ensuring both paths were tested.

The most challenging aspect was covering error handling paths. Many error scenarios required specific setup...

## Challenges Encountered

The most significant challenge was... Testing private methods presented a dilemma... Mocking time-based functionality required...

## Benefits of Mocking

Mocking external dependencies transformed the testing process in several ways:

1. **Speed**: Tests run in under 1 second instead of waiting for actual database/API calls
2. **Isolation**: Failures clearly indicate which component has issues
3. **Flexibility**: Can easily test error scenarios that are hard to reproduce with real services

However, mocking also introduced complexity...

## Coverage vs Quality Trade-offs

While pursuing high coverage, I discovered that not all coverage is created equal. Some tests I wrote achieved coverage but provided minimal value...

I believe 85-90% coverage is the sweet spot. Beyond that, the effort required...

## Lessons Learned

The most important insight from this assignment is that coverage is a tool, not a goal. High coverage doesn't guarantee quality, but it does...

If I were to approach a similar project in the future, I would...

## Conclusion

White box testing with code coverage metrics provides valuable feedback, but must be balanced with other quality measures...
```

### 5.3 Grading Criteria (10 points)

- **Content Quality** (5 pts): Addresses all required sections thoroughly
- **Insights** (3 pts): Demonstrates deep understanding, not just surface-level observations
- **Writing Quality** (2 pts): Clear, concise, professional, 400-600 words

---

## 📤 Deliverables

### GitHub Repository Structure

```
homework-5-taskflow/
├── README.md
├── requirements.txt (or package.json)
├── .gitignore
├── src/
│   ├── task.py (or task.js)
│   ├── task_service.py (or taskService.js)
│   ├── task_repository.py (or taskRepository.js)
│   ├── notification_service.py (or notificationService.js)
│   └── __init__.py (if Python)
├── tests/
│   ├── test_task_unit.py (or task.test.js)
│   ├── test_task_service_integration.py (or taskService.test.js)
│   ├── test_coverage_edge_cases.py (or coverageEdgeCases.test.js)
│   ├── test_mocking.py (or mocking.test.js)
│   └── conftest.py (or jest.config.js)
├── reports/
│   ├── coverage-analysis.md
│   ├── analysis-report.md
│   └── screenshots/
│       ├── coverage-summary.png
│       ├── coverage-html-report.png
│       └── test-execution.png
├── htmlcov/ (or coverage/)
│   └── index.html (generated)
└── .github/
    └── workflows/
        └── tests.yml (optional - for bonus)
```

### README Requirements

Your README must include:

1. Project description and objectives
2. Prerequisites (Python 3.11+/Node 22+, pytest/Jest)
3. Installation instructions
4. How to run tests
5. How to generate coverage reports
6. Coverage summary (current metrics)
7. Project structure explanation
8. Key features implemented

### Example README:

````markdown
# Homework 5: White Box Testing - TaskFlow System

## Description

Comprehensive white box test suite for a task management system demonstrating unit testing, integration testing, code coverage analysis, and mocking techniques.

## Objectives

- Achieve >85% statement coverage and >80% branch coverage
- Implement isolated unit tests for all model methods
- Create integration tests with proper mocking
- Analyze and document coverage gaps

## Prerequisites

- Python 3.11+ (or Node.js 22+)
- pytest and pytest-cov (or Jest)

## Installation

```bash
# Python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# JavaScript
npm install
```

## Running Tests

```bash
# Python - Run all tests
pytest -v

# Python - With coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Python - Specific test file
pytest tests/test_task_unit.py -v

# JavaScript - Run all tests
npm test

# JavaScript - With coverage
npm test -- --coverage

# JavaScript - Watch mode
npm test -- --watch
```

## Coverage Reports

After running tests with coverage:

```bash
# Python
open htmlcov/index.html

# JavaScript
open coverage/lcov-report/index.html
```

## Current Coverage

- **Statement Coverage**: 91%
- **Branch Coverage**: 84%
- **Function Coverage**: 95%
- **Line Coverage**: 90%

## Project Structure

- `src/` - Production code (Task, TaskService, etc.)
- `tests/` - Test suite (unit, integration, mocking tests)
- `reports/` - Coverage analysis and screenshots
- `htmlcov/` or `coverage/` - Generated coverage reports

## Features Implemented

- ✅ Task model with validation and state management
- ✅ TaskService with business logic
- ✅ Complete unit test suite (15+ tests)
- ✅ Integration tests with mocking (10+ tests)
- ✅ Comprehensive coverage analysis
- ✅ Error scenario testing

## Test Summary

- **Total Tests**: 27
- **Unit Tests**: 15
- **Integration Tests**: 12
- **All Tests Passing**: ✅

## Author

[Your Name] - Software Testing Fall 2026
````

---

## 📤 Submission Requirements

### GitHub Repository

1. Create a new public repository named `taskflow-white-box-tests` or similar
2. Include all files listed in the Deliverables structure
3. Ensure all tests pass: `pytest` or `npm test`
4. Generate final coverage report
5. Commit frequently with meaningful messages
6. Tag your final submission: `git tag -a hw5-final -m "Homework 5 submission"`

### Canvas Submission

Submit:

1. **GitHub Repository URL** (including tag)
2. **Coverage Analysis Report** (PDF export)
3. **Analysis Report** (PDF)
4. **Brief Reflection** (200-300 words):
   - What was most challenging about achieving high coverage?
   - How does white box testing differ from black box testing?
   - Will you use code coverage in your future projects?

---

## 🎯 Grading Rubric

| **Category**                | **Points** | **Criteria**                                                              |
| --------------------------- | ---------- | ------------------------------------------------------------------------- |
| **Unit Tests**              | 20         | 15+ tests, >90% model coverage, complete isolation, proper assertions     |
| **Integration Tests**       | 25         | 10+ tests, workflows, mocking, >85% branch coverage, error scenarios      |
| **Coverage Analysis**       | 25         | >85% statement, >80% branch, HTML reports, gap analysis, justification    |
| **Mocking & Isolation**     | 20         | Proper mocks, test doubles, error scenarios, fast execution, verification |
| **Analysis Report**         | 10         | 400-600 words, addresses all sections, thoughtful insights                |
| **Documentation & Quality** | 5          | Clean code, good README, organization, commit messages                    |
| **Code Quality**            | 5          | Production-ready code, proper structure, naming conventions               |
| **Total**                   | **110**    | (10 bonus points included)                                                |

### Detailed Grading Criteria

**Excellent (90-100%)**:

- Exceeds all coverage targets (>90% statement, >85% branch)
- Comprehensive test suite with excellent test design
- Professional-grade mocking and isolation
- Deep, insightful analysis
- Production-ready code quality
- Exceptional documentation

**Good (80-89%)**:

- Meets all coverage targets
- Complete test coverage with good design
- Proper mocking and test isolation
- Good analysis with solid insights
- Clean, well-organized code
- Good documentation

**Satisfactory (70-79%)**:

- Meets minimum requirements
- Adequate test coverage
- Basic mocking implemented
- Acceptable analysis
- Code works but could be cleaner
- Basic documentation

**Needs Improvement (<70%)**:

- Below coverage targets
- Incomplete or failing tests
- Poor or missing mocking
- Superficial analysis
- Code quality issues
- Inadequate documentation

---

## 🎁 Bonus Opportunities (+10 points)

### Bonus Option 1: Dual Implementation (+5 points)

Implement the system in **BOTH Python AND JavaScript**:

- Both must have equivalent functionality
- Both must have equivalent test suites
- Both must achieve coverage targets
- Document implementation differences
- Compare testing frameworks (pytest vs Jest)

### Bonus Option 2: CI/CD with Coverage Tracking (+3 points)

Set up GitHub Actions for automated testing and coverage:

- Create `.github/workflows/tests.yml`
- Run tests on every push and pull request
- Generate coverage reports automatically
- Upload to Codecov or Coveralls
- Add coverage badge to README
- Enforce minimum coverage thresholds

Example workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

      - name: Check coverage thresholds
        run: |
          pytest --cov=src --cov-fail-under=85
```

### Bonus Option 3: Mutation Testing (+2 points)

Use mutation testing to verify test quality:

- Install mutation testing framework (mutmut for Python or Stryker for JavaScript)
- Run mutation tests on your code
- Document mutation score (target >80%)
- Analyze surviving mutants
- Explain why some mutants survived

**Python**:

```bash
pip install mutmut
mutmut run
mutmut results
mutmut html
```

**JavaScript**:

```bash
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner
npx stryker run
```

Include mutation testing report in your submission.

---

## 💡 Tips for Success

1. **Start with the model** - Get Task class working and fully tested first
2. **Test as you code** - Don't write all code then all tests
3. **Use TDD approach** - Write failing test, make it pass, refactor
4. **Run coverage early** - Check coverage after every few tests
5. **Focus on branches** - If/else, switch statements need both paths tested
6. **Mock everything external** - Database, network, file system, time
7. **Test error paths** - Don't just test happy paths
8. **Keep tests fast** - Full suite should run in under 1 second
9. **Name tests clearly** - Should describe exactly what is being tested
10. **Use fixtures** - Reduce duplication with proper test setup

### Coverage Tips

11. **Target branches first** - Branch coverage is harder than statement coverage
12. **Use coverage report** - HTML report shows exactly which lines are missed
13. **Test all conditions** - Every if/elif/else path needs coverage
14. **Test exception handling** - Try/except blocks need both paths tested
15. **Don't chase 100%** - Some code (like logging) doesn't need coverage

### Mocking Tips

16. **Mock at boundaries** - Mock database, API, external services
17. **Don't mock what you test** - Only mock dependencies, not the unit under test
18. **Verify interactions** - Use assert_called_with to verify mock usage
19. **Test mock failures** - Simulate errors with side_effect
20. **Use appropriate doubles** - Mock for verification, stub for data, fake for complex behavior

---

## ⚠️ Common Mistakes to Avoid

- ❌ **Writing tests after all code** - Test as you go for better coverage
- ❌ **Not mocking external dependencies** - Tests will be slow and unreliable
- ❌ **Only testing happy paths** - Must test error scenarios
- ❌ **Ignoring branch coverage** - Statement coverage alone is insufficient
- ❌ **Testing implementation details** - Test behavior, not internal structure
- ❌ **Duplicate test logic** - Use fixtures and helper methods
- ❌ **Poor test names** - Name should describe what is tested and expected outcome
- ❌ **Tests depend on each other** - Each test must be completely independent
- ❌ **Not verifying mock calls** - Using mocks without asserting they were called correctly
- ❌ **Chasing 100% coverage** - Diminishing returns, focus on quality
- ❌ **Ignoring coverage gaps** - Must document and justify untested code
- ❌ **Tests that don't fail** - Write failing test first to verify it works

---

## 🆘 Getting Help

If you're stuck:

1. Review the [Module 5 theory materials](../theory/)
2. Check the [white box testing exercises](../exercises/) for examples
3. Read testing framework documentation:
   - [pytest documentation](https://docs.pytest.org/)
   - [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
   - [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
   - [Jest documentation](https://jestjs.io/)
   - [Jest mocking guide](https://jestjs.io/docs/mock-functions)
4. Ask questions in the course discussion forum
5. Attend office hours
6. Review the example code structures provided above

---

## 📚 Resources

### White Box Testing

- [Module 5 Theory - Unit Testing](../theory/01-unit-testing.md)
- [Module 5 Theory - Code Coverage](../theory/02-code-coverage.md)
- [Module 5 Theory - Mocking](../theory/03-mocking.md)
- [Module 5 Theory - Integration Testing](../theory/04-integration-testing.md)

### Testing Frameworks

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Coverage Plugin](https://pytest-cov.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Jest Documentation](https://jestjs.io/)
- [Jest Mock Functions](https://jestjs.io/docs/mock-functions)

### Code Coverage

- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Istanbul (JavaScript Coverage)](https://istanbul.js.org/)
- [Understanding Coverage Metrics](https://www.atlassian.com/continuous-delivery/software-testing/code-coverage)

### Mocking & Test Doubles

- [Martin Fowler - Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [Test Doubles - xUnit Patterns](http://xunitpatterns.com/Test%20Double.html)

---

## ✅ Submission Checklist

Before submitting, verify:

### Implementation (Parts 1-2)

- [ ] Task model implemented with all required fields
- [ ] Task validation logic implemented (title length, due date)
- [ ] Status transition logic implemented and enforced
- [ ] TaskService implemented with business logic
- [ ] TaskRepository interface created (for mocking)
- [ ] NotificationService interface created (for mocking)

### Unit Tests (Part 1)

- [ ] At least 15 unit tests implemented
- [ ] All Task model methods tested
- [ ] Validation tests for all rules
- [ ] Status transition tests for all paths
- [ ] Priority comparison tests
- [ ] Overdue detection tests
- [ ] All unit tests passing
- [ ] > 90% statement coverage on models

### Integration Tests (Part 2)

- [ ] At least 10 integration tests implemented
- [ ] TaskService with TaskRepository tested
- [ ] Complete workflows tested (create → update → complete)
- [ ] Business rule enforcement tested
- [ ] NotificationService properly mocked
- [ ] TaskRepository properly mocked
- [ ] Error scenarios tested (database failures, API failures)
- [ ] All integration tests passing
- [ ] > 85% branch coverage overall

### Coverage Analysis (Part 3)

- [ ] Coverage reports generated (HTML + terminal)
- [ ] > 85% statement coverage achieved
- [ ] > 80% branch coverage achieved
- [ ] Screenshots of coverage reports included
- [ ] Untested code paths identified and documented
- [ ] Justification provided for any gaps
- [ ] Coverage improvement strategy documented

### Mocking & Isolation (Part 4)

- [ ] All external dependencies mocked
- [ ] Proper use of mocks (verification)
- [ ] Proper use of stubs (return values)
- [ ] Error scenarios tested with mocks
- [ ] Mock interactions verified (assert_called_with)
- [ ] Tests run fast (<1 second total)
- [ ] Tests completely isolated (no shared state)

### Reports (Part 5)

- [ ] Coverage analysis report completed
- [ ] Analysis report written (400-600 words)
- [ ] All required sections addressed
- [ ] Insights demonstrate understanding
- [ ] Professional writing quality

### Repository & Documentation

- [ ] Complete README with setup instructions
- [ ] All files organized in correct structure
- [ ] requirements.txt or package.json with all dependencies
- [ ] .gitignore configured properly (exclude htmlcov/, coverage/, **pycache**, node_modules/)
- [ ] Repository is public and accessible
- [ ] Meaningful commit messages throughout
- [ ] Code is clean and well-formatted

### Final Checks

- [ ] All tests pass: `pytest -v` or `npm test`
- [ ] Coverage meets targets: `pytest --cov=src` or `npm test -- --coverage`
- [ ] No skipped or xfail tests
- [ ] Coverage reports generated successfully
- [ ] Final commit tagged (hw5-final)
- [ ] Repository URL ready for submission
- [ ] Reflection document written (200-300 words)

---

**Good luck!** This homework will deepen your understanding of white box testing, code coverage, and test isolation. Remember: high coverage is a means to finding bugs, not an end in itself. Focus on writing meaningful tests that actually validate behavior, and the coverage will follow! 🎯
