# Homework 5: White Box Testing - TaskFlow System

## Description

White box test suite for **TaskFlow**, a task management system. The project contains the
production code (model, repository, notification service, business-logic service) and a test
suite that demonstrates unit testing, integration testing with mocks, test doubles
(mocks, stubs, fakes) and code coverage analysis.

## Objectives

- Achieve >80% statement, branch and function coverage
- Isolated unit tests for every Task model method
- Integration tests of `TaskService` with mocked repository and notification service
- Analyse and document coverage gaps

## Prerequisites

- Python 3.11+
- pytest and pytest-cov (installed from `requirements.txt`)

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

```bash
# All tests
pytest -v

# With coverage (terminal + HTML)
pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html

# A single file
pytest tests/test_task_unit.py -v
```

## Coverage Reports

```bash
pytest --cov=src --cov-branch --cov-report=html
open htmlcov/index.html   # generated on every run, not committed
```

## Current Coverage

- **Statement Coverage**: 100% (234 statements)
- **Branch Coverage**: 100% (74 branches)
- **Function Coverage**: 100% (33 functions)
- **Line Coverage**: 100%

## Test Summary

| File                                   | Focus                                              | Tests |
| -------------------------------------- | -------------------------------------------------- | ----- |
| `tests/test_task_unit.py`              | Task model, fully isolated                         | 37    |
| `tests/test_task_service_integration.py` | TaskService + mocked repository/notifier         | 24    |
| `tests/test_mocking.py`                | Stubs, mocks, fakes, error scenarios, isolation    | 23    |
| `tests/test_coverage_edge_cases.py`    | Repository, notification service, service branches | 35    |
| **Total**                              | All passing, about 0.4 s                           | **119** |

## Project Structure

```
src/
  task.py                  Task model, enums, validation, transitions, overdue, priority
  task_repository.py       Data layer (CRUD, search/filter) over an injected database
  notification_service.py  Email/SMS through an injected transport, with retries
  task_service.py          Business rules; orchestrates repository and notifications
tests/                     Unit, integration, mocking and edge-case tests + conftest.py
reports/                   coverage-analysis.md, analysis-report.md, reflection.md, screenshots/
pytest.ini                 testpaths = tests, pythonpath = . src
```

## Features Implemented

- ✅ Task model with title/due-date validation, forward-only status transitions, overdue detection and priority comparison
- ✅ Unique titles, soft delete (ARCHIVED is terminal and frozen), field updates with validation
- ✅ Search by status, priority, due-date range and partial title, combinable
- ✅ Overdue check that notifies the user
- ✅ Notification failures never break the workflow (logged and swallowed)
- ✅ URGENT tasks also trigger an SMS
- ✅ Error scenarios tested with `side_effect` (database failures, SMTP/SMS failures, retries)

## Author

dakewer.cinco - Software Testing Fall 2026
