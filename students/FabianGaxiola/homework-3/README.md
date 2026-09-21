# Homework 3: Static Testing Setup

**Student**: Fabian Gaxiola
**Project**: budget calculator
**Language**: Python

## Description

app in python to help manage income and outcome

## Setup Instructions

1. python -m venv .venv
2. .venv\Scripts\activate
3. pip install -r requirements.txt
4. pre-commit install
5. python -m src.main

## Pre-commit Hooks Configured

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black]

  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
```

## Linting

pylint .\src\main.py > pylint-report.txt
