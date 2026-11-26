# Homework 5: White Box Testing - TaskFlow System

## Description

White box test suite for TaskFlow, a small task management system: a `Task` model with
validation and a guarded status lifecycle, a `TaskRepository` data layer, a
`NotificationService` gateway, and a `TaskService` that orchestrates them. The tests cover
unit-level logic, service integration with mocked dependencies, test doubles (mock, stub, fake),
failure injection, and statement/branch coverage analysis.

## Objectives

- Exceed 80% statement and branch coverage (achieved 100% / 100%)
- Isolated unit tests for every `Task` method
- Integration tests where external dependencies are mocked
- Document coverage and what it does not prove

## Prerequisites

- Python 3.11+ (the code is also verified on Python 3.9)
- `pytest` and `pytest-cov`

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v                       # all tests
pytest tests/test_task_unit.py  # one file
pytest --cov=src --cov-branch --cov-report=term-missing
```

`pytest.ini` sets `pythonpath = . src`, so plain `pytest` works from this directory.

## Coverage Reports

```bash
pytest --cov=src --cov-branch --cov-report=html
open htmlcov/index.html   # macOS; use xdg-open on Linux
```

`htmlcov/` is generated on every run and is not committed. Text captures of a run are in
`reports/screenshots/`.

## Current Coverage

- **Statement Coverage**: 100% (234/234)
- **Branch Coverage**: 100% (78/78)
- **Function / Line Coverage**: 100%
- **Tests**: 130 passing, about 0.1–0.3 s for the full suite

## Project Structure

- `src/task.py` - Task model, enums, validation, transitions, overdue detection, priority sort
- `src/task_repository.py` - data layer over an injected database; wraps failures in `RepositoryError`
- `src/notification_service.py` - email/SMS gateway over injected transport clients
- `src/task_service.py` - business rules; injectable clock; notification failures never break a workflow
- `tests/test_task_unit.py` - 43 isolated model tests
- `tests/test_task_service_integration.py` - 37 workflow tests (mocked notifier, real repository over a fake database)
- `tests/test_mocking.py` - 24 tests of mocks, stubs, fakes, failure injection and call order
- `tests/test_coverage_edge_cases.py` - 26 tests for gateway and repository branches
- `tests/conftest.py` - fixed clock, `FakeDatabase`, mock fixtures
- `reports/` - coverage analysis, analysis report, reflection, terminal captures

## Features Implemented

- Task creation with unique, 3-100 character titles and future-only due dates
- Status lifecycle TODO → IN_PROGRESS → DONE, archive from any open state, ARCHIVED terminal
- Atomic task updates (all fields validated before any is applied)
- Soft delete (archive) and purge restricted to archived tasks
- Overdue detection with per-task notifications
- Search by status, priority, due-date range and partial title, ordered by priority
- Email on create/status change, plus SMS for URGENT tasks
- Error scenarios: repository failures propagate without notifying; notification failures are logged and swallowed

## Design Notes

- Dependencies and the clock are injected so every test is deterministic and isolated.
- Titles are unique case-insensitively, ignoring surrounding whitespace.
- The duplicate-title check is check-then-act and not safe under concurrent writers; a real
  database would need a unique constraint (see `reports/coverage-analysis.md`).

## Author

Isaac Vazquez (isaac-evs) - Software Testing Fall 2026
