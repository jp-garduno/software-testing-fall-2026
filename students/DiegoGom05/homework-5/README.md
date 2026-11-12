# Homework 5: White Box Testing - TaskFlow System

## Description

White box test suite for TaskFlow, a task management system. It demonstrates unit
testing, integration testing, code coverage analysis and mocking techniques.

## Objectives

- Achieve >80% statement and branch coverage (achieved 100%)
- Isolated unit tests for every model method
- Integration tests with mocked repository and notification service
- Analyze and document coverage gaps

## Prerequisites

- Python 3.11+ (tested on 3.10)
- pytest and pytest-cov

## Installation

```bash
python -m venv venv
source venv/bin/activate   # Windows (Git Bash): source venv/Scripts/activate
python -m pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
pytest tests/test_task_unit.py -v
```

## Coverage Reports

```bash
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
open htmlcov/index.html   # Windows: start htmlcov/index.html
```

## Current Coverage

- **Statement Coverage**: 100%
- **Branch Coverage**: 100%
- **Function Coverage**: 100%
- **Line Coverage**: 100%

## Project Structure

- `src/task.py` - Task model: validation, transitions, overdue, priority
- `src/task_service.py` - Business logic orchestrating repository and notifications
- `src/task_repository.py` - Data layer interface (mocked in tests)
- `src/notification_service.py` - External notification interface (mocked in tests)
- `tests/test_task_unit.py` - Unit tests for the model
- `tests/test_task_service_integration.py` - Integration tests with mocks
- `tests/test_mocking.py` - Mocks, stubs, fakes and error scenarios
- `tests/test_coverage_edge_cases.py` - Extra branch coverage
- `tests/conftest.py` - Shared fixtures
- `reports/` - Coverage analysis, analysis report, reflection and screenshots

## Features Implemented

- ✅ Task model with validation and state machine
- ✅ TaskService with creation, update, soft delete, overdue check, search and filters
- ✅ Email and SMS notifications that never break the workflow
- ✅ Unit, integration and mocking test suites
- ✅ Error scenario testing (database and notification failures)

## Test Summary

- **Total Tests**: 119
- **All Tests Passing**: ✅

## Author

Diego Gomez - Software Testing Fall 2026
