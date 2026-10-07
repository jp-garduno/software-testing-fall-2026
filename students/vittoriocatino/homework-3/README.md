# Homework 3: Static Testing Setup

**Student**: Vittorio Catino
**Project**: In-Memory Task Tracker
**Language**: Python

## Description

This project is a small, dependency-free task tracker used to demonstrate a
complete static-testing workflow. It validates task input, normalizes tags,
tracks a task's completion state, and provides summary information through a
testable service layer.

## Setup Instructions

From the repository root, install the project tools and the hooks:

```bash
cd students/vittoriocatino/homework-3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ../../..
pre-commit install --config students/vittoriocatino/homework-3/.pre-commit-config.yaml
```

Run all configured hooks from the repository root:

```bash
pre-commit run --all-files --config students/vittoriocatino/homework-3/.pre-commit-config.yaml
```

## Pre-commit Hooks Configured

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-json`
- `check-added-large-files`
- `black`
- `isort`
- `pylint`
- `bandit`

The Python-specific hooks are scoped to this submission directory so the
course repository's unrelated examples are not changed by this project setup.

## Testing

Run the tests and coverage report from this directory:

```bash
pytest -q --cov=src --cov-report=term-missing
```

Run the individual static-analysis tools:

```bash
pylint --rcfile=.pylintrc src test_task_service.py
black --check src test_task_service.py
isort --check-only --profile black src test_task_service.py
bandit -q -r src
```

The final local run has 14 passing tests, 100% source coverage, a Pylint score
of 10.00/10, and no Bandit findings.
