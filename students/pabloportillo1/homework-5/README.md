# Homework 5: White Box Testing — TaskFlow Task Management

**Student**: Pablo Portillo
**Module**: 5 — White Box Testing & Coverage

## Description

TaskFlow, the task management system described in
[homework-5.md](../../../05-white-box-testing/homework/homework-5.md), implemented in Python together
with a white box test suite: isolated unit tests for the model, integration tests across the service
and repository, mocking tests for every external dependency, and boundary tests aimed at the branches
and limits of each business rule.

### Objectives

- Over 80% statement, branch and function coverage, measured with coverage.py
- Unit tests for every method of the `Task` model, isolated from the clock and from storage
- Integration tests for complete workflows with the repository and notification service replaced
  only at their external edges
- Documented coverage gaps and a measured improvement strategy

## Coverage Summary

| Metric    | Achieved             |
| --------- | -------------------- |
| Statement | 100% (273/273)       |
| Branch    | 100% (78/78)         |
| Function  | 100% (39/39)         |
| Line      | 100% (273/273)       |
| Tests     | 169 passed in 0.38s  |
| Pylint    | 10.00/10 (course configuration) |

| Test file                               | Tests | Focus                                                   |
| --------------------------------------- | ----: | ------------------------------------------------------- |
| `tests/test_task_unit.py`               |    51 | `Task` model: validation, transitions, overdue, priority |
| `tests/test_task_service_integration.py`|    24 | `TaskService` + real `TaskRepository` + fake database    |
| `tests/test_mocking.py`                 |    30 | Mocks, stubs and a spy; failure paths and call order     |
| `tests/test_coverage_edge_cases.py`     |    64 | Boundary values and branch-by-branch checks              |

The full analysis, including how coverage grew step by step and a mutation check showing what
coverage alone misses, is in [reports/coverage-analysis.md](reports/coverage-analysis.md).

## Prerequisites

- Python 3.11+
- pytest and pytest-cov (`requirements.txt`)

## Installation

```bash
# From this directory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Tests

```bash
# All tests
python -m pytest -v

# One file
python -m pytest tests/test_task_unit.py -v
```

`pytest.ini` puts `.` and `src/` on the import path, so plain `pytest` works the same way.

## Coverage Reports

```bash
# Terminal report with missing lines and branches (what the grading workflow measures)
python -m pytest --cov=src --cov-branch --cov-report=term-missing

# HTML report, then open htmlcov/index.html
python -m pytest --cov=src --cov-branch --cov-report=html
open htmlcov/index.html
```

`htmlcov/` is generated on every run and ignored by git; the screenshots in `reports/screenshots/`
are the committed evidence.

## Project Structure

```
homework-5/
├── src/
│   ├── task.py                    # Task model, TaskStatus, TaskPriority, lifecycle rules
│   ├── task_repository.py         # TaskRepository, TaskFilter, Database protocol
│   ├── notification_service.py    # NotificationService, gateway protocols, retries
│   └── task_service.py            # TaskService: business rules and orchestration
├── tests/
│   ├── conftest.py                # Fixtures: frozen clock, fakes and autospec mocks
│   ├── doubles.py                 # FrozenClock, FakeDatabase, shared constants
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

## Design

Each layer receives its dependencies in its constructor, so a test replaces exactly one external
edge and keeps everything else real:

```
TaskService ──> TaskRepository ──> Database          (external: database driver)
     └────────> NotificationService ──> EmailGateway (external: email provider)
                                   └──> SmsGateway   (external: SMS provider)
```

The assignment's example stubs `TaskRepository` and `NotificationService` with methods that only
raise `NotImplementedError`. Here they are thin real layers instead: the repository assigns ids,
filters, sorts and turns `DatabaseError` into `RepositoryError`; the notification service validates
addresses, truncates SMS and retries failed provider calls. That gives both of them logic worth white
box testing, while the database and the providers stay mocked.

| Test double | Where | Used for |
| ----------- | ----- | -------- |
| Mock        | `create_autospec(...)` of `TaskRepository`, `NotificationService`, `Database` and the gateways | Verifying calls, arguments and order (`attach_mock`) |
| Stub        | `return_value` / `side_effect` on those mocks | Canned results and simulated failures |
| Fake        | `FakeDatabase` | Working in-memory storage for the integration tests |
| Spy         | `Mock(wraps=FakeDatabase())` | Real behaviour while recording calls |
| Patched clock | `FrozenClock` over `task.datetime` | Fixed, movable "now" for every time-based rule |

## Business Rules Implemented

- **Creation**: title 3-100 characters after trimming surrounding spaces, unique ignoring case;
  description up to 500 characters (longer is rejected, not truncated); due date optional but, when
  given, strictly later than now; new tasks start in TODO with `created_at` set.
- **Updates**: title, description, priority and due date, validated together so an invalid value
  changes nothing; a new title must still be unique; `updated_at` is stamped; archived tasks cannot
  be edited.
- **Lifecycle**: TODO → IN_PROGRESS → DONE, ARCHIVED from any state, nothing out of ARCHIVED; every
  status change notifies the owner.
- **Deletion**: `delete_task` archives (soft delete); `purge_task` removes the task permanently.
- **Overdue**: due date in the past and status neither DONE nor ARCHIVED; `check_overdue_tasks`
  notifies the owner about each overdue task it finds and returns them.
- **Search**: by status, priority, inclusive due date range and case-insensitive partial title, in
  any combination; results sorted URGENT > HIGH > MEDIUM > LOW, ties in insertion order; tasks
  without a due date are left out when a date range is given.
- **Notifications**: email to the owner for every event; URGENT tasks also by SMS when the owner has
  a phone number; SMS over 160 characters is cut with `...`; failed provider calls are retried up to
  3 times; a notification that still fails is logged and never undoes or blocks the task change.

## Author

Pablo Portillo — Software Testing, Fall 2026
