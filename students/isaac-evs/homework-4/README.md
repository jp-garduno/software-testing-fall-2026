# Homework 4: Black Box Testing - SecureBank System

## Description

Comprehensive black box test suite for SecureBank, a simulated online banking
system, using Equivalence Partitioning (EP), Boundary Value Analysis (BVA),
Decision Tables, and State Transition Testing. Covers account transfers,
deposits, freeze/unfreeze, account closure, monthly fee processing, bill
payment validation, and transaction history filtering.

## Prerequisites

- Python 3.11+ (developed and verified against Python 3.9's stdlib feature
  set, no version-specific syntax is used)
- `pytest` and `pytest-cov`

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage (terminal + HTML report)
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
```

## Viewing the Coverage Report

After running the command above, open `htmlcov/index.html` in a browser.
`htmlcov/` is a regenerated build artifact and is excluded from the
repository via `.gitignore`; text captures of a prior run are checked in at
`reports/screenshots/test-results.txt` and
`reports/screenshots/coverage-report.txt` for reference.

## Project Structure

- `design/` — Test design documentation (EP, BVA, decision tables, state transitions)
- `src/` — SecureBank banking system implementation (`banking_system.py`)
- `tests/` — Automated test suite (pytest)
- `reports/` — Test execution report, analysis report, and reflection

## What Was Tested

- `BankAccount.transfer()` — amount validity, sufficient funds, daily limit,
  account state (Active/Frozen/Suspended/Closed)
- `BankAccount.deposit()` — restoring a Suspended account to Active
- `BankAccount.freeze()` / `unfreeze()` — including the balance-dependent
  outcome of unfreezing (Active vs. Suspended)
- `BankAccount.close()` — the terminal Closed state and its rejection of all
  further operations
- `BankAccount.apply_monthly_fee()` — waiver threshold, insufficient-funds
  suspension, and Premium's permanent $0 fee
- `validate_account_type()`, `validate_bill_payment()`,
  `filter_transactions_by_date()` — standalone validation helpers

## Test Coverage

- Equivalence Partitioning: 23 tests
- Boundary Value Analysis: 21 tests
- Decision Tables: 16 tests
- State Transitions: 15 tests
- **Total**: 75 tests, 100% line coverage on `src/banking_system.py`

## Author

Isaac Vazquez (isaac-evs)
