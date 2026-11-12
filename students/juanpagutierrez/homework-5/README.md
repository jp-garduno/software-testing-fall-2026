# Homework 5: White Box Testing - TaskFlow System

**Student**: Juan Pablo Gutierrez
**Language**: Python 3.11

## Description

TaskFlow is a small task management system (task model, repository, business
service and notification service) built from scratch for this assignment,
together with a white box test suite that covers every statement and every
branch of the production code. External dependencies, the database client and
the email/SMS providers, are replaced by test doubles so the whole suite runs
in well under a second.

## Objectives

- Reach >80% statement and >80% branch coverage (achieved: 100% / 100%)
- Unit test every method of the `Task` model in complete isolation
- Integration test `TaskService` with mocked repository and notifications
- Use mocks, stubs and fakes deliberately, including failure scenarios
- Analyze and document coverage gaps and how they were closed

## Prerequisites

- Python 3.11+
- pytest and pytest-cov (installed from `requirements.txt`)

## Installation

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

Run every command from this `homework-5/` directory. `pytest.ini` sets
`testpaths = tests` and `pythonpath = . src`, so plain `pytest` works.

```bash
# All tests
pytest -v

# One suite
pytest tests/test_task_unit.py -v

# Lint with the course configuration
pylint --rcfile=../../../.github/grading/pylintrc src tests
```

## Coverage Reports

```bash
# Terminal report with statement + branch coverage and missing lines
pytest --cov=src --cov-branch --cov-report=term-missing

# HTML report (written to htmlcov/, which is git-ignored)
pytest --cov=src --cov-branch --cov-report=html
# then open htmlcov/index.html
```

## Current Coverage

| Metric             | Achieved          |
| ------------------ | ----------------- |
| Statement Coverage | 100% (267/267)    |
| Branch Coverage    | 100% (76/76)      |
| Function Coverage  | 100% (39/39)      |
| Line Coverage      | 100%              |
| Pylint (course rc) | 10.00/10          |

Full analysis: [reports/coverage-analysis.md](reports/coverage-analysis.md).

## Test Summary

| Suite                                    | Tests | Focus                                                        |
| ---------------------------------------- | ----- | ------------------------------------------------------------ |
| `tests/test_task_unit.py`                | 52    | Task model: validation, transitions, overdue, priority       |
| `tests/test_task_service_integration.py` | 25    | TaskService workflows with mocked repository + notifications |
| `tests/test_mocking.py`                  | 19    | Failure scenarios, call order, fake repository, real layers  |
| `tests/test_coverage_edge_cases.py`      | 46    | Boundaries, query filters, repository and notification edges |
| **Total**                                | **142** | All passing, ~0.3 s without coverage                       |

## Project Structure

```
homework-5/
├── src/
│   ├── task.py                  # Task model, TaskStatus, TaskPriority
│   ├── task_repository.py       # TaskRepository + TaskQuery (search/filter)
│   ├── task_service.py          # Business rules, orchestration, error translation
│   └── notification_service.py  # Email/SMS wrapper around provider clients
├── tests/
│   ├── conftest.py              # Fixed clock, mocks, FakeTaskRepository
│   ├── test_task_unit.py
│   ├── test_task_service_integration.py
│   ├── test_mocking.py
│   └── test_coverage_edge_cases.py
└── reports/
    ├── coverage-analysis.md
    ├── analysis-report.md
    ├── reflection.md
    └── screenshots/
```

## Key Features Implemented

- ✅ Task model with title/description/due date validation
- ✅ Forward-only status lifecycle; ARCHIVED reachable from any state and terminal
- ✅ Overdue detection (past due and not DONE/ARCHIVED) with notifications
- ✅ Priority comparison and sorting (URGENT > HIGH > MEDIUM > LOW)
- ✅ Unique titles on create and rename
- ✅ Soft delete (archive) plus explicit permanent purge of archived tasks
- ✅ Search by status, priority, inclusive date range and partial title, combinable
- ✅ Repository failures translated to `ServiceUnavailableError`
- ✅ Notification failures logged and recorded without breaking the workflow
- ✅ SMS in addition to email for urgent tasks (and overdue HIGH/URGENT tasks)

### Design decisions that make the code testable

- **Injectable clock**: `TaskService(clock=...)` and `Task(now=...)` let tests pin
  time to a fixed instant, so overdue and due-date tests never flake.
- **Narrow boundaries**: `TaskRepository` only talks to a `database` client and
  `NotificationService` only to `email_client` / `sms_client`. Those clients are
  the only things that ever need mocking at the lowest level.
- **One error type per layer**: `RepositoryError` and `NotificationError` let the
  service decide which failures are fatal (storage) and which are not (delivery).

## Author

Juan Pablo Gutierrez - Software Testing Fall 2026
