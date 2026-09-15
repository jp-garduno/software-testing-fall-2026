# Homework 3: Static Testing Setup

**Student**: Juan Pablo Gutierrez
**Project**: Task Manager CLI
**Language**: Python

## Description

A small command-line task manager that lets you add, list, complete, remove,
and summarize tasks stored in a local JSON file. It was written specifically
for this assignment, with a few intentional style/quality issues that were
later found and fixed with the linters below.

## Setup Instructions

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```
3. Run the project:
   ```bash
   cd src
   python cli.py add "Buy groceries" --priority high
   python cli.py list
   python cli.py done 1
   python cli.py summary
   ```

## Pre-commit Hooks Configured

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-json`
- `check-added-large-files`
- `black` (code formatter)
- `isort` (import sorter)
- `pylint` (linter)
- `bandit` (security linter, bonus)

## Linting

Run the linters manually with:

```bash
black src/
isort --profile=black src/
pylint src/*.py
bandit -r src/
```

Or run everything (including the pre-commit hooks) against all files with:

```bash
pre-commit run --all-files
```

See [REPORT.md](./REPORT.md) for the full static analysis report, including
the issues that were found and how they were fixed, and
[STYLE_GUIDE.md](./STYLE_GUIDE.md) for the team style guide (bonus).

## CI/CD (bonus)

A GitHub Actions workflow at
[`.github/workflows/homework-3-juanpagutierrez.yml`](../../../.github/workflows/homework-3-juanpagutierrez.yml)
runs Black, isort, Pylint and Bandit on every push/PR that touches this
directory.
