# Homework 5: White Box Testing — TaskFlow System

**Student:** Luis Cacho (`LuisCacho-py`)  
**Module:** 5 — White Box Testing & Coverage

---

## Description

Comprehensive white box test suite for the **TaskFlow Task Management System**, demonstrating isolated unit testing, component integration testing, test doubles (`Mock`), and statement/branch coverage analysis.

## Objectives

- Achieve >85% statement coverage and >80% branch coverage (achieved **100%** in both)
- Implement isolated unit tests for all `Task` model methods (15 tests)
- Implement integration and mocking tests for `TaskService`, `TaskRepository`, and `NotificationService` (12 tests)
- Document coverage metrics and white box testing analysis

## Prerequisites

- Python 3.11+
- `pytest` and `pytest-cov`

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests
pytest -v

# Run with statement and branch coverage
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

## Current Coverage

| Metric             | Threshold | Achieved | Status  |
| ------------------ | --------- | -------- | ------- |
| Statement Coverage | 85%       | 100%     | ✅ Pass |
| Branch Coverage    | 80%       | 100%     | ✅ Pass |
| Function Coverage  | 90%       | 100%     | ✅ Pass |
| Line Coverage      | 85%       | 100%     | ✅ Pass |

## Project Structure

```
homework-5/
├── README.md
├── requirements.txt
├── pyproject.toml
├── conftest.py
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── task.py
│   ├── task_repository.py
│   ├── notification_service.py
│   └── task_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_task_unit.py
│   └── test_task_service_integration.py
└── reports/
    ├── coverage-analysis.md
    └── analysis-report.md
```

## Test Summary

- **Total Tests**: 27
- **Unit Tests**: 15 (`tests/test_task_unit.py`)
- **Integration & Mocking Tests**: 12 (`tests/test_task_service_integration.py`)
- **All Tests Passing**: ✅ (0.17s)
