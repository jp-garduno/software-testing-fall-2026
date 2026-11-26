# Homework 3: Static Testing Setup

**Student**: Frijol
**Project**: Todo List CLI (demo project)
**Language**: Python

## Description

Small command-line to-do list app used to calibrate the static testing setup
(pre-commit, linting) before applying it to the main project.

## Setup Instructions

1. `pip install -r requirements.txt`
2. `pre-commit install`
3. `python src/cli.py`

## Pre-commit Hooks Configured

- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- check-added-large-files
- black
- isort
- pylint

## Linting

Run `pylint src/*.py` and `black --check src/` manually, or let pre-commit
run them automatically on commit. Run `pre-commit run --all-files` to check
every file at once.
