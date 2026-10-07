# Homework 4: Black Box Testing — SecureBank

Black box test suite for an online banking system, designed with equivalence
partitioning, boundary value analysis, decision tables and state transition
testing, and implemented with pytest.

**Author**: Emmanuel Arias (`yair91`) · Module 4 · Fall 2026

## What was tested

SecureBank has three account types (Savings, Checking, Premium), each with its
own minimum balance, monthly fee and daily transfer limit, and four account
states (Active, Suspended, Frozen, Closed). The suite covers transfers, deposits,
bill payments with immediate and future scheduling, the monthly fee run, and the
transaction history with date filtering and CSV export.

The design and every expected result live in
[`design/test-design-document.md`](design/test-design-document.md). Each test
carries its design id in the docstring (`EP1`, `BV13`, `DT1-R4`, `ST9`), so a
failure points back to the rule it came from.

## Results

|                              |                           |
| ---------------------------- | ------------------------- |
| Tests                        | 87, all passing           |
| Line coverage of `src/`      | 100% (139/139 statements) |
| pylint, course configuration | 10.00/10                  |

| Technique                | Tests  | Coverage on its own |
| ------------------------ | ------ | ------------------- |
| Equivalence partitioning | 23     | 76%                 |
| Boundary value analysis  | 23     | 47%                 |
| Decision tables          | 24     | 70%                 |
| State transitions        | 17     | 65%                 |
| **Together**             | **87** | **100%**            |

## Prerequisites

- Python 3.9 or newer (the course targets 3.11+; the code avoids syntax newer
  than 3.9 so it runs on both)
- The packages in `requirements.txt`

## Installation

```bash
cd students/yair91/homework-4
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the tests

```bash
pytest -v
```

With coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

An HTML coverage report, written to `htmlcov/index.html`:

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html          # Linux: xdg-open
```

One technique at a time:

```bash
pytest tests/test_equivalence_partitioning.py -v
pytest tests/test_boundary_values.py -v
pytest tests/test_decision_tables.py -v
pytest tests/test_state_transitions.py -v
```

Linting, with the same configuration the grading workflow uses:

```bash
pylint --rcfile=../../../.github/grading/pylintrc src tests conftest.py
```

`pytest.ini` puts the submission root on `sys.path`, so `from src.banking_system
import BankAccount` resolves no matter which directory you launch pytest from
inside the submission. `conftest.py` at the root does the same thing as a
fallback for older pytest versions.

## Project structure

```
homework-4/
├── README.md                          this file
├── conftest.py                        puts the submission root on sys.path
├── pytest.ini                         pytest configuration
├── requirements.txt
├── design/
│   └── test-design-document.md        Part 1: EP, BVA, decision tables, states
├── src/
│   ├── __init__.py
│   └── banking_system.py              the system under test
├── tests/
│   ├── conftest.py                    shared fixtures
│   ├── test_equivalence_partitioning.py
│   ├── test_boundary_values.py
│   ├── test_decision_tables.py
│   └── test_state_transitions.py
└── reports/
    ├── test-execution-report.md       Part 3: results and coverage analysis
    ├── analysis-report.md             Part 4: technique comparison
    ├── reflection.md
    ├── logs/                          raw pytest, coverage and pylint output
    └── screenshots/
```

## Documents

- [Test design document](design/test-design-document.md) — Part 1
- [Test execution report](reports/test-execution-report.md) — Part 3
- [Analysis report](reports/analysis-report.md) — Part 4
- [Reflection](reports/reflection.md)
