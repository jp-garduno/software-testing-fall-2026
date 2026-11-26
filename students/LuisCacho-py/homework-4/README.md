# Homework 4: Black Box Testing — SecureBank System

**Student:** Luis Cacho (`LuisCacho-py`)
**Module:** 4 — Black Box Testing

---

## Description

Comprehensive black box test suite for the **SecureBank Online Banking System**
using four systematic techniques:

- **Equivalence Partitioning (EP)** — 18 tests
- **Boundary Value Analysis (BVA)** — 17 tests
- **Decision Tables (DT)** — 17 tests
- **State Transition Testing (ST)** — 19 tests
- **Total:** 71 automated tests, all passing

**Coverage:** 83% line coverage on `src/`

---

## Prerequisites

- Python 3.11+
- pip

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running Tests

```bash
# All tests (verbose)
pytest -v

# With coverage report (terminal)
pytest --cov=src --cov-report=term-missing

# With HTML coverage report
pytest --cov=src --cov-report=html
# → Open htmlcov/index.html in your browser
```

---

## Project Structure

```
homework-4/
├── README.md                          # This file
├── requirements.txt                   # pytest, pytest-cov
├── pyproject.toml                     # pytest + bandit config
├── .gitignore
├── design/
│   └── test-design-document.md       # Part 1: EP, BVA, DT, ST documentation
├── src/
│   ├── __init__.py
│   └── banking_system.py             # BankAccount + BankingSystem implementation
├── tests/
│   ├── conftest.py                   # Shared fixtures
│   ├── test_equivalence_partitioning.py  # 18 EP tests
│   ├── test_boundary_values.py           # 17 BVA tests
│   ├── test_decision_tables.py           # 17 DT tests
│   └── test_state_transitions.py         # 19 ST tests
└── reports/
    ├── test-execution-report.md      # Part 3: Results + coverage analysis
    └── analysis-report.md            # Part 4: Technique comparison (600 words)
```

---

## System Under Test Summary

**SecureBank** supports three account types:

| Account Type | Min Balance | Monthly Fee | Fee Waiver (balance >) | Daily Transfer Limit |
|-------------|-------------|-------------|------------------------|----------------------|
| Savings     | $100        | $5.00       | $1,000                 | $2,000               |
| Checking    | $0          | $10.00      | $5,000                 | $5,000               |
| Premium     | $10,000     | $0.00       | N/A                    | $50,000              |

**Account States:** Active → Suspended / Frozen → Closed (terminal)

---

## Key Business Rules Tested

1. Minimum transfer amount: $0.01
2. Cannot transfer from Frozen or Closed accounts
3. Daily transfer limits reset at midnight
4. Fee waived if balance **strictly greater than** threshold
5. Insufficient fee funds → account suspended
6. Closed accounts cannot be re-opened (terminal state)

---

## Test Results

```
71 passed in ~0.15s
Coverage: 83% (src/)
```

---

## Author

**Luis Cacho** — `LuisCacho-py`  
Module 4: Black Box Testing, Software Testing Fall 2026
