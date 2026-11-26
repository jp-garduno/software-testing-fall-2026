# Homework 5: TaskFlow White Box Testing

## Description

TaskFlow is a small task-management system implemented and tested for the White Box Testing module. It demonstrates isolated unit tests, mocked integration boundaries, coverage analysis, state-machine testing, and error handling.

## Prerequisites and installation

- Python 3.11 or newer
- `pip`

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run tests and coverage

```bash
python -m pytest -v
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
open htmlcov/index.html
```

## Coverage summary

The suite is designed to exceed 85% statement coverage, 80% branch coverage, and 90% function coverage. See [coverage-analysis.md](reports/coverage-analysis.md) for methodology and remaining infrastructure scope.

## Project structure

```text
homework-5/
├── src/       # Task model, service, repository, notification boundary
├── tests/     # Unit, integration, edge-case, and mocking tests
└── reports/   # Coverage and white-box analysis reports
```

## Key features

- Validated task titles, priorities, due dates, and descriptions
- Forward-only task lifecycle plus terminal archival
- Overdue detection and priority comparison
- Task creation, updates, soft deletion, filtering, and overdue workflows
- Repository and notification isolation via strict mocks
