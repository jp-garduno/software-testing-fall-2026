# Homework 4: Black Box Testing — SecureBank

## Description

Comprehensive black-box testing suite for an online banking system. The project applies:

- Equivalence Partitioning (EP)
- Boundary Value Analysis (BVA)
- Decision Tables
- State Transition Testing

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run all tests

```bash
pytest tests/ -v
```

## Run with coverage

```bash
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

Then open:

```text
htmlcov/index.html
```

## Project structure

```text
homework-4/
├── README.md
├── design/
│   └── test-design-document.md
├── src/
│   ├── __init__.py
│   └── banking_system.py
├── tests/
│   ├── conftest.py
│   ├── test_equivalence_partitioning.py
│   ├── test_boundary_values.py
│   ├── test_decision_tables.py
│   └── test_state_transitions.py
├── reports/
│   ├── test-execution-report.md
│   ├── analysis-report.md
│   ├── reflection.md
│   └── screenshots/
├── requirements.txt
└── .gitignore
```

## What is tested

The suite validates transfer amounts, account types, minimum balances, daily limits,
fee-waiver thresholds, bill-payment conditions, date ranges, and account-state transitions.

## Suggested submission path

Place this folder under:

```text
students/<your-github-username>/homework-4/
```

## Author

Carlos Emiliano Olmedo Navarro
