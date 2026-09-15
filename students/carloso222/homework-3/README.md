# Homework 3: Static Testing Setup

**Student**: Carlos Emiliano Olmedo Navarro
**Project**: Python Calculator with Validation and History
**Language**: Python

## Description

A simple calculator library with three modules: `calculator.py` (basic
arithmetic operations), `validator.py` (input validation helpers), and
`history.py` (operation history tracking with JSON export). The project is
fully covered by static testing tooling (Pylint, Black, isort) wired up
through `pre-commit`.

## Setup Instructions

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```
3. Run the project's tests to confirm everything works (see Testing below).

## Pre-commit Hooks Configured

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-json`
- `check-added-large-files`
- `black` (code formatting)
- `isort` (import sorting, black-compatible profile)
- `pylint` (static analysis, using `.pylintrc`)

## Testing

Run the full test suite with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run linting manually:

```bash
pylint src/*.py --rcfile=.pylintrc
```

Run formatting checks:

```bash
black --check src/ tests/
isort --check-only --profile=black src/ tests/
```

See `REPORT.md` for the full static analysis write-up, including issues
found, fixes applied, and recommendations.
