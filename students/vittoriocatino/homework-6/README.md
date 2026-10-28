# Library Management System

A small library-management system built with a test-driven workflow for Homework 6.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Verification

```bash
python -m pytest -q
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

The project is organised as `src/` for domain code, `tests/` for independent pytest cases, and `docs/` for the documented Red-Green-Refactor cycles and reflection.
