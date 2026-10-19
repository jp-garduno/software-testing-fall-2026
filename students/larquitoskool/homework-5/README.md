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

```

## Running Tests

```bash
# Python - Run all tests
pytest -v

# Python - With coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Python - Specific test file
pytest tests/test_task_unit.py -v

```

## Coverage Reports

After running tests with coverage:

```bash
# Python
open htmlcov/index.html

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

Carlos Ariel Rubio Espinosa - Software Testing Fall 2026