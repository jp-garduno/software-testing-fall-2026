# Homework 4: Black Box Testing - SecureBank System

## Description

This project implements a black box testing suite for the SecureBank Online Banking System.

The test suite applies four black box testing techniques:

- Equivalence Partitioning
- Boundary Value Analysis
- Decision Table Testing
- State Transition Testing

The system under test simulates banking operations such as account creation, transfers, deposits, bill payments, monthly fee processing, and account state changes.

The final automated suite contains **40 tests**, all passing, with **100% code coverage**.

## Prerequisites

- Python 3.11 or newer
- pip
- Python virtual environment recommended

The project was tested using Python 3.13.9.

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run tests with coverage:

```bash
python -m pytest --cov=src --cov-branch --cov-report=term --cov-report=html
```

## Viewing the Coverage Report

After running the coverage command, an HTML report is generated inside:

```text
htmlcov/
```

Open the following file in a browser:

```text
htmlcov/index.html
```

The final test execution achieved **100% coverage**.

## What Was Tested

### Equivalence Partitioning

Tests representative valid and invalid classes such as:

- Valid transfer amounts
- Zero and negative transfer amounts
- Transfers exceeding available balance or daily limits
- Invalid account types
- Invalid initial balances
- Invalid deposits
- Invalid payees

### Boundary Value Analysis

Tests values around important banking boundaries, including:

- Minimum valid transfer amount
- Checking daily transfer limit
- Savings daily transfer limit
- Minimum account balances
- Monthly fee waiver thresholds

### Decision Table Testing

Tests combinations of business conditions for:

- Transfer validation
- Monthly fee processing
- Bill payment validation
- Account restrictions

### State Transition Testing

Tests behavior across the following account states:

- Active
- Suspended
- Frozen
- Closed

Transitions such as Active to Frozen, Active to Suspended, Suspended to Active, Frozen to Active, and transitions to Closed are validated.

## Test Results

| Metric | Result |
|---|---:|
| Total tests | 40 |
| Passed | 40 |
| Failed | 0 |
| Code coverage | 100% |

## Project Structure

```text
homework-4/
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
│   └── screenshots/
│       ├── test-results.png
│       └── coverage-report.png
├── requirements.txt
├── .gitignore
└── README.md
```

## Documentation

Detailed test design is available in:

```text
design/test-design-document.md
```

Execution results and coverage evidence are available in:

```text
reports/test-execution-report.md
```

The analysis of the black box testing techniques is available in:

```text
reports/analysis-report.md
```

## Author

Luis-045