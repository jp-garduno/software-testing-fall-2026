# Homework 5: White Box Testing - TaskFlow System

## Description

TaskFlow is a small task-management system used to demonstrate white-box unit
testing, integrated business workflows, branch coverage, and isolated
dependency testing.

## Objectives

- Validate task data and lifecycle transitions.
- Exercise task service workflows with a local repository.
- Isolate notification and repository failures with standard-library mocks.
- Measure statement, branch, and function coverage.

## Prerequisites

- Python 3.11 or newer.
- The test suite uses only `unittest` and `unittest.mock` from the Python
  standard library.
- `coverage` is an optional development tool used only to generate the coverage
  report; it is not imported by any test.

## Installation

From this directory, create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

The test suite needs no package installation. To generate coverage reports,
install the optional reporting tool:

```powershell
python -m pip install coverage
```

`requirements.txt` is intentionally free of third-party test dependencies.

## Running Tests

Run all tests using the standard library:

```powershell
python -m unittest discover -s tests -v
```

If `pytest` is already available in the grading environment, the included
`pytest.ini` also supports:

```powershell
pytest -v
```

## Coverage Reports

From this directory, run:

```powershell
python -m coverage erase
python -m coverage run --branch --source=src -m unittest discover -s tests -q
python -m coverage report -m
python -m coverage html
```

Open `htmlcov/index.html` to inspect the generated HTML report. Generated
coverage data is ignored by Git.

## Current Coverage

Measured with `coverage.py` 7.16.2 across the 64 standard-library tests:

| Metric             |         Result |
| ------------------ | -------------: |
| Statement coverage | 100% (227/227) |
| Branch coverage    |   100% (92/92) |
| Function coverage  |   100% (27/27) |
| Line coverage      |           100% |

## Project Structure

- `src/` contains the task model, in-memory repository, notification boundary,
  and service workflows.
- `tests/` contains model unit tests, service integration tests, mocking tests,
  and coverage edge cases.
- `reports/` contains coverage analysis, the two written reflections, and
  screenshots of the coverage and test results.

## Features Implemented

- Task validation, priorities, due-date checks, and one-way status transitions.
- In-memory CRUD, exact-title uniqueness, and combined search filters.
- Task creation, field updates, archival, completion, and overdue notifications.
- Mocked repository/provider failures and interaction-order verification.
- HTML coverage report with all tracked statements and branches exercised.

## Test Summary

- Total tests: 64.
- Unit tests: 32.
- Integration tests: 12.
- Mocking tests: 7.
- Coverage edge-case tests: 13.
- External test dependencies: none.

## Author

Fabian Gaxiola - Software Testing Fall 2026
