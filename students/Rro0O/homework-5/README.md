# Homework 5: White Box Testing - TaskFlow System

## Description

White box test suite for **TaskFlow**, a task management system (Task model, TaskService, TaskRepository and
NotificationService), covering unit tests, integration tests with mocks, coverage analysis and test-double usage.

## Objectives

- Reach >80% statement, branch and function coverage (achieved 100% on all three)
- Isolated unit tests for every `Task` method
- Integration tests for `TaskService` with mocked repository and notifications
- Document coverage, gaps and strategy

## Prerequisites

- Python 3.11+ (also runs on 3.9)
- pytest and pytest-cov

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
pytest tests/test_task_unit.py -v
```

## Coverage Reports

```bash
pytest --cov=src --cov-branch --cov-report=html --cov-report=term-missing
open htmlcov/index.html
```

## Current Coverage

| Metric             | Value |
| ------------------ | ----- |
| Statement Coverage | 100%  |
| Branch Coverage    | 100%  |
| Function Coverage  | 100%  |
| Line Coverage      | 100%  |

## Project Structure

- `src/` - `task.py`, `task_service.py`, `task_repository.py`, `notification_service.py`
- `tests/` - `test_task_unit.py`, `test_task_service_integration.py`, `test_mocking.py`,
  `test_coverage_edge_cases.py`, `conftest.py`
- `reports/` - `coverage-analysis.md`, `analysis-report.md`, `reflection.md`, `screenshots/`

## Features Implemented

- Task model: validation, status transitions, overdue detection, priority comparison
- TaskService: create (unique title), update, status changes, soft delete, overdue check, search/filter, SMS for URGENT
- Notification failures are logged and never break a workflow
- Mocks, stubs and a fake repository for test isolation

## Test Summary

- **Total Tests**: 74 (all passing, <0.5 s)
- **Unit**: 32 (`test_task_unit.py`)
- **Integration**: 24 (`test_task_service_integration.py`)
- **Mocking / error scenarios**: 12 (`test_mocking.py`)
- **Coverage edge cases**: 6 (`test_coverage_edge_cases.py`)

## Author

Rogelio Sosa (Rro0O) - Software Testing Fall 2026
