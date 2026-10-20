# Homework 5: White Box Testing — TaskFlow

## Description

TaskFlow is a small task management system (tasks with validation, a status
lifecycle, priorities, overdue detection, search and notifications) built
from scratch to practice white box testing: isolated unit tests, integration
tests with test doubles, branch-coverage analysis and mocking of external
dependencies.

## Objectives

- Reach more than 80% statement, branch and function coverage of `src/`
- Unit test every method of the `Task` model in complete isolation
- Integration test `TaskService` together with `TaskRepository` and `NotificationService`
- Mock every external dependency (database, email and SMS clients, the clock)
- Document coverage gaps and how they were closed

## Prerequisites

- Python 3.11+
- pytest and pytest-cov (`requirements.txt`)

## Installation

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Running Tests

Run every command from this `homework-5/` folder. `pytest.ini` adds `.` and
`src` to the import path, so plain `pytest` works.

```bash
# All tests
pytest -v

# One file
pytest tests/test_task_unit.py -v

# With statement + branch coverage (same flags as the grading system)
pytest -v --cov=src --cov-branch --cov-report=term-missing
```

## Coverage Reports

```bash
pytest --cov=src --cov-branch --cov-report=html --cov-report=term-missing
# then open htmlcov/index.html  (Windows: start htmlcov\index.html)
```

`htmlcov/` is generated on every run and is ignored by git; the evidence is in
`reports/screenshots/`.

## Current Coverage

| Metric             | Achieved                |
| ------------------ | ----------------------- |
| Statement coverage | **100%** (247/247)      |
| Branch coverage    | **100%** (70/70)        |
| Function coverage  | **100%** (38/38)        |
| Line coverage      | **100%**                |
| Pylint (course rc) | **10.00/10**            |
| Suite run time     | **≈ 0.3 s** (133 tests) |

Details and the improvement history are in
[`reports/coverage-analysis.md`](reports/coverage-analysis.md).

## Project Structure

```
homework-5/
├── README.md
├── requirements.txt
├── pytest.ini                 # testpaths = tests, pythonpath = . src
├── .gitignore
├── src/
│   ├── errors.py              # domain exceptions
│   ├── task.py                # Task model, TaskStatus, TaskPriority
│   ├── task_repository.py     # data layer: CRUD, search/filter, DB error wrapping
│   ├── notification_service.py # email/SMS gateway over injected clients
│   └── task_service.py        # business rules, orchestrates repository + notifications
├── tests/
│   ├── conftest.py            # fixtures, fixed clock, FakeDatabase
│   ├── test_task_unit.py                  # Part 1 – 56 unit tests
│   ├── test_task_service_integration.py   # Part 2 – 29 integration tests
│   ├── test_coverage_edge_cases.py        # Part 3 – 33 gap-closing tests
│   └── test_mocking.py                    # Part 4 – 15 mocking / isolation tests
└── reports/
    ├── coverage-analysis.md
    ├── analysis-report.md
    ├── reflection.md
    └── screenshots/
```

## Design Decisions

- **Dependency injection everywhere.** The repository receives a `database`
  object, the notification service receives `email_client`/`sms_client`, and
  the service receives the repository, the notifier and a `clock`. This is
  what makes every layer testable without patching.
- **Controllable time.** `Task` methods accept `now=`, and `TaskService`
  takes a `clock` callable. Tests use a fixed `NOW`, so they never depend on
  the real date (no flaky "overdue" tests, no bypassing validation).
- **One error type per layer.** Database failures become `RepositoryError`,
  delivery failures become `NotificationError`.
- **Notifications never break a workflow.** If saving fails nothing is
  notified; if notifying fails the change is kept and a warning is logged.

## Features Implemented

- ✅ Task model: title (3–100), description (≤ 500), priority, future due date, timestamps
- ✅ Forward-only status lifecycle with ARCHIVED as terminal state
- ✅ Overdue detection (past due and not DONE/ARCHIVED)
- ✅ Priority comparison and sorting URGENT > HIGH > MEDIUM > LOW
- ✅ Unique titles (case-insensitive) on create and update
- ✅ Soft delete (archive) and permanent delete (purge)
- ✅ Search by status, priority, date range and partial title, combinable
- ✅ Email on create / status change / overdue, plus SMS for URGENT tasks
- ✅ Unit, integration, edge-case and mocking test suites

## Test Summary

| Suite                                               | Tests   |
| --------------------------------------------------- | ------- |
| Unit (`test_task_unit.py`)                          | 56      |
| Integration (`test_task_service_integration.py`)    | 29      |
| Coverage edge cases (`test_coverage_edge_cases.py`) | 33      |
| Mocking & isolation (`test_mocking.py`)             | 15      |
| **Total — all passing**                             | **133** |

No skipped or xfail tests.

## Author

Carlos Olmedo (carloso222) — Software Testing Fall 2026
