# Homework 3: Static Testing Setup

**Student:** Luis-045
**Project:** Todo List
**Language:** Python

## Project Description

This project is a simple task management application developed in Python.

The application allows users to create tasks, assign priorities, mark tasks as completed, remove tasks, and display a summary of the current task list.

The main purpose of this project is to practice static testing by configuring and using tools such as Pylint, Black, isort, and pre-commit hooks.

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

The project contains 8 unit tests.

Run all tests with:

```bash
python -m unittest -v
```

The expected result is:

```text
Ran 8 tests

OK
```

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

Example:

```text
feat: add initial project setup
fix: resolve linting issues
docs: add analysis report
```

## Final Results

After correcting the static analysis issues:

```text
Unit tests: 8 passed
Pre-commit hooks: Passed
Pylint score: 10.00/10
```

The static testing tools helped identify formatting problems, unused code, import problems, long lines, and other code quality issues before committing the final version of the project.
