# Homework 4: Black Box Testing — SecureBank Online Banking

[![Homework 4 Black Box Suite](https://github.com/jp-garduno/software-testing-fall-2026/actions/workflows/homework-4-pabloportillo.yml/badge.svg)](https://github.com/jp-garduno/software-testing-fall-2026/actions/workflows/homework-4-pabloportillo.yml)

**Student**: Pablo Portillo
**Module**: 4 — Black Box Testing

## Description

A complete black box test suite for the SecureBank online banking system described in
[homework-4.md](../../../04-black-box-testing/homework/homework-4.md). The system under test
implements the three account types, the four account states, the transfer, bill payment, monthly
fee and transaction history rules; the suite exercises it with all four black box techniques —
equivalence partitioning, boundary value analysis, decision tables and state transition testing.

The same 116 test cases are implemented twice, in Python with pytest and in JavaScript with Jest,
so the design can be compared across two frameworks (bonus option 1). Both suites run in GitHub
Actions on every push and pull request that touches this directory (bonus option 2), and the state
model is drawn as a Mermaid diagram in the design document (bonus option 3).

| | Python | JavaScript |
| --- | --- | --- |
| Tests | 116 passed | 116 passed |
| Line coverage | 100% | 100% |
| Branch coverage | 100% | 99.15% |
| Static analysis | pylint 10.00/10, black, isort | eslint clean, prettier clean |

## Prerequisites

- Python 3.11+ (the suite is also valid on newer versions)
- Node.js 22+ for the JavaScript mirror suite

## Installation

```bash
# From this directory
pip install -r requirements.txt

# JavaScript suite
cd js && npm install
```

The repository root already provides Jest, so `npx jest` works from the repository root without a
separate install.

## Running the tests

```bash
# Python, verbose
pytest -v

# Python, with branch coverage (this is what CI runs)
pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=90

# JavaScript
cd js && npx jest --config jest.config.js --verbose

# JavaScript with coverage
cd js && npx jest --config jest.config.js --coverage
```

## Viewing the coverage report

```bash
# Python HTML report -> reports/htmlcov/index.html
pytest --cov=src --cov-branch --cov-report=html:reports/htmlcov

# JavaScript HTML report -> js/coverage/lcov-report/index.html
cd js && npx jest --config jest.config.js --coverage
```

Coverage output is generated, not committed; the console output of the run described in the
execution report is committed under `reports/logs/` as evidence.

## Static analysis

```bash
pylint --rcfile=.pylintrc src tests
black --check --line-length=120 src tests
isort --check-only --profile=black --line-length=120 src tests
npx eslint js --ext .js
npx prettier --check "js/src/**/*.js" "js/tests/**/*.js"
```

## Project structure

```
homework-4/
├── README.md
├── design/
│   └── test-design-document.md    # Part 1: EP, BVA, decision tables, state transitions
├── src/
│   ├── __init__.py
│   └── banking_system.py          # System under test (Python)
├── tests/
│   ├── conftest.py
│   ├── test_equivalence_partitioning.py
│   ├── test_boundary_values.py
│   ├── test_decision_tables.py
│   └── test_state_transitions.py
├── js/
│   ├── src/bankingSystem.js       # System under test (JavaScript mirror)
│   ├── tests/*.test.js            # The same 116 cases in Jest
│   ├── jest.config.js
│   └── package.json
├── reports/
│   ├── test-execution-report.md   # Part 3
│   ├── analysis-report.md         # Part 4
│   ├── reflection.md              # Canvas reflection
│   ├── dual-implementation-notes.md
│   ├── logs/                      # Raw console output
│   └── screenshots/               # Terminal captures
├── requirements.txt
├── pyproject.toml
├── .pylintrc
└── .gitignore
```

## What was tested

| Technique | Design IDs | Tests |
| --------- | ---------- | ----- |
| Equivalence Partitioning | EP1–EP35 | 36 |
| Boundary Value Analysis  | BV1–BV31 | 33 |
| Decision Tables          | DT1–DT4 (28 rules) | 31 |
| State Transitions        | ST1–ST13 | 16 |
| **Total**                |          | **116** |

Every test docstring names the design ID it implements, so a failing test points straight at the
row of the design table it came from. The design assumptions that resolve the ambiguities in the
assignment brief are listed in section 0 of the design document.

## Author

Pablo Portillo — ITESO, Software Testing Fall 2026
