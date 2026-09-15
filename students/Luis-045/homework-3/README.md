# Homework 3: Static Testing Setup

**Student:** Luis-045
**Project:** Todo List
**Language:** Python

## Project Description

This project is a simple task management application developed in Python.

The application allows users to create tasks, assign priorities, mark tasks as completed, remove tasks, filter tasks by priority, calculate completion statistics, and display a summary of the current task list.

The main purpose of this project is to practice static testing by configuring and using tools such as Pylint, Black, isort, coverage, and pre-commit hooks.

## Project Structure

```text
homework-3/
├── .pre-commit-config.yaml
├── .pylintrc
├── .gitignore
├── README.md
├── REPORT.md
├── requirements.txt
├── test_task_manager.py
└── src/
    ├── __init__.py
    ├── app.py
    ├── task.py
    └── task_manager.py
```

## Setup Instructions

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Install the pre-commit hooks:

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

## Running the Application

The application can be executed with:

```bash
python -m src.app
```

## Running the Tests

The project contains 23 unit tests.

Run all tests with:

```bash
python -m unittest -v
```

The expected result is:

```text
Ran 23 tests

OK
```

## Test Coverage

Coverage is measured using the `coverage` package.

Run the tests with coverage enabled:

```bash
coverage run --source=src -m unittest
```

Display the coverage report with:

```bash
coverage report -m
```

The final coverage result is:

```text
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/__init__.py           0      0   100%
src/app.py               20      1    95%   30
src/task.py              18      0   100%
src/task_manager.py      54      0   100%
---------------------------------------------------
TOTAL                    92      1    99%
```

The project achieved 99% total source code coverage.

## Static Analysis

Pylint is used to analyze the Python source code.

Run Pylint manually with:

```bash
pylint src
```

The Pylint configuration is stored in the `.pylintrc` file.

The project uses a maximum line length of 88 characters and disables some documentation-related warnings for this small project.

## Code Formatting

Black is used to automatically format Python files.

Run Black manually with:

```bash
black .
```

isort is used to automatically organize Python imports.

Run isort manually with:

```bash
isort --profile=black .
```

## Pre-commit Hooks

The project uses the following pre-commit hooks:

- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- check-added-large-files
- check-merge-conflict
- detect-private-key
- Black
- isort
- Pylint
- conventional-pre-commit

The hooks are scoped to:

```text
students/Luis-045/homework-3/
```

This prevents the hooks from modifying or analyzing files that belong to other parts of the repository.

All hooks can be executed manually with:

```bash
pre-commit run --all-files
```

The `conventional-pre-commit` hook is also configured to validate commit messages using the Conventional Commits format.

Examples:

```text
feat: add initial project setup
fix: resolve linting issues
test: improve source code coverage
docs: add analysis report
```

## Final Results

After correcting the static analysis issues and improving the test suite:

```text
Unit tests: 23 passed
Test coverage: 99%
Pre-commit hooks: Passed
Pylint score: 10.00/10
```

The static testing tools helped identify formatting problems, unused code, import problems, long lines, and other code quality issues before committing the final version of the project.

The additional unit tests also increased source code coverage from approximately 64% to 99%.
