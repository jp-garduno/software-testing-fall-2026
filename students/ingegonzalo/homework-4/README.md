# Homework 4: Black Box Testing - SecureBank System

## Description

Comprehensive black box test suite for SecureBank, an online banking system,
using the four core black box testing techniques: Equivalence Partitioning (EP),
Boundary Value Analysis (BVA), Decision Tables, and State Transition Testing.

## Prerequisites

- Python 3.11+
- pytest and pytest-cov

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# All tests
pytest -v

# With coverage (terminal + HTML report)
pytest -v --cov=banking_system --cov-report=html --cov-report=term
```

## Viewing the Coverage Report

After running the command above with `--cov-report=html`, open the generated report:

```bash
# Windows
start htmlcov\index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

## Project Structure

- `design/` - Test design documentation (EP, BVA, Decision Tables, State Transitions)
- `src/` - Banking system implementation (`banking_system.py`)
- `tests/` - Automated test suite (pytest)
- `reports/` - Test execution report and analysis report

## Test Coverage

| Technique               | Tests |
|--------------------------|-------|
| Equivalence Partitioning | 6     |
| Boundary Value Analysis  | 21    |
| Decision Tables          | 5     |
| State Transitions        | 5     |
| **Total**                | **39**|

Line coverage: 78% (see `reports/test-execution-report.md` for full coverage analysis).

## What Was Tested

The `BankAccount` class models three account types (Savings, Checking, Premium),
each with its own minimum balance, monthly fee, fee waiver threshold, and daily
transfer limit. Core behaviors under test:

- Transfers: amount validation, sufficient funds, account state, and daily limit checks
- Bill payments: payee validation, amount validation, sufficient funds
- Monthly fee processing: charged or waived based on balance vs. threshold
- Account state transitions: Active, Suspended, Frozen, Closed, including invalid
  transitions (e.g., attempting a transfer on a Closed or Frozen account)

## Author

ingegonzalo