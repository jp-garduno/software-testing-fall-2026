# Homework 4: Black Box Testing - SecureBank System

[![Homework 4 tests](https://github.com/Rro0O/software-testing-fall-2026/actions/workflows/homework-4-rro0o.yml/badge.svg?branch=feat/rro0o/homework-4)](https://github.com/Rro0O/software-testing-fall-2026/actions/workflows/homework-4-rro0o.yml)

**Student**: Rogelio Sosa (Rro0O)  **Languages**: Python (primary) + JavaScript (dual implementation bonus)

## Description

Comprehensive black box test suite for SecureBank, an online banking system (Savings / Checking / Premium accounts,
Active / Frozen / Suspended / Closed states, transfers, bill payments, monthly fees, transaction history and CSV export).
The tests were designed from the specification with **Equivalence Partitioning, Boundary Value Analysis, Decision Tables
and State Transition testing**, then implemented in pytest and, equivalently, in Jest.

## Prerequisites

- Python 3.11+ (developed on 3.9 - no newer syntax is used) and `pytest`, `pytest-cov`
- Node.js 22+ (for the JavaScript port)

## Installation

```bash
# Python
pip install -r requirements.txt

# JavaScript
npm install
```

## Running tests

```bash
# Python - all tests
pytest -v

# Python - with coverage (statements + branches)
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html

# JavaScript - tests + coverage
npm test
```

## Viewing the coverage report

Python: open `htmlcov/index.html` after running the coverage command. JavaScript: the table is printed by `npm test`
and the HTML report is written to `coverage/lcov-report/index.html`.

## Extra: mutation check

`python tools/mutation_check.py` injects 16 deliberate defects into `src/banking_system.py` and shows which test file
detects each one (all 16 are killed).

## Project structure

```
design/test-design-document.md   Part 1 - EP, BVA, decision tables, state transitions (Mermaid diagram included)
src/banking_system.py            System under test (Python)      src/bankingSystem.js  (JavaScript port)
tests/test_*.py                  pytest suites + conftest.py     tests/*.test.js       Jest suites (+ jest.setup.js)
tools/mutation_check.py          Test-effectiveness check
reports/test-execution-report.md, analysis-report.md, reflection.md, screenshots/
../../../.github/workflows/homework-4-rro0o.yml   CI (bonus; lives at the repo root so GitHub runs it)
```

## What was tested

| Technique | Python tests | Jest tests |
|-----------|-------------:|-----------:|
| Equivalence partitioning (EP1-EP37) | 46 | 47 |
| Boundary value analysis (BV1-BV59) | 59 | 59 |
| Decision tables (4 tables) | 44 | 44 |
| State transitions (ST1-ST25) | 34 | 34 |
| **Total** | **183** | **184** |

Every test docstring / name starts with its design ID (`EP7`, `BV29`, `DT2-R6`, `ST17`, ...).
Assumptions made where the statement is ambiguous are listed in section 0 of the design document.

## Author

Rogelio Sosa
