# Homework 3: Static Testing Setup

**Student**: Isaac Vazquez (isaac-evs)
**Project**: Calculator, Task Manager & String Utils
**Language**: Python

## Description

A small Python utility library with three modules — a `Calculator` with operation history, a `TaskManager` for tracking to-do items with priorities, and a set of `string_utils` helper functions. The project exists to demonstrate a complete static testing setup: pre-commit hooks, linting configuration, and a before/after analysis of the issues found.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install pre-commit hooks (run from this directory, treated as the project root):
   ```bash
   pre-commit install
   ```
3. Run the project's tests:
   ```bash
   pytest -v
   ```

## Pre-commit Hooks Configured

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-json`
- `check-added-large-files`
- `black` (code formatting)
- `isort` (import sorting, black profile)
- `pylint` (static analysis, using `.pylintrc`)

## Linting Configuration

- `.pylintrc` — generated with `pylint --generate-rcfile`, `max-line-length=100`
- Formatting handled by `black` (line length 88, default) and `isort --profile=black`

## Testing

```bash
pytest -v
```

23 tests covering `Calculator`, `TaskManager`, and `string_utils`, all passing.

## Linting Reports

- `pylint-report-before.txt` — baseline report before any fixes (score: 6.51/10)
- `pylint-report-after.txt` — report after fixes and formatting (score: 10.00/10)

See `REPORT.md` for the full analysis of issues found, fixes applied, and lessons learned.
