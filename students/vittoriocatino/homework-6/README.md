# Library Management System

A small library-management system built with a test-driven workflow for Homework 6.

## Features

- Catalog, availability, member limits, borrowing, returns, and title/author search.
- Advanced features: category-based member policies and late fees, plus FIFO book
  reservations with notification of the next waiting member.
- 38 independent tests, HTML coverage evidence, five documented TDD cycles, and
  a short reflection in `docs/`.

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

Open `coverage/index.html` after the coverage command to inspect the HTML report.

The project is organised as `src/` for domain code, `tests/` for independent pytest cases, and `docs/` for the documented Red-Green-Refactor cycles and reflection.
