# Homework 3: Static Testing Setup

**Student**: Emmanuel Arias (`yair91`)
**Project**: Inventory — stock control for a small warehouse
**Language**: Python

## Description

A small inventory module: a product catalogue with stock levels, a log of
stock movements in and out, and reports for low stock and valuation. The
project exists to have real code for the static analysis tools to work on, so
the first version was written with the kind of mistakes that get written for
real.

## Results

```
pylint before   6.10/10   48 findings across 19 codes
pylint after    10.00/10  0 findings
bandit          0 security issues over 122 lines
pre-commit      13 hooks, all passing
```

The full before and after output is in [`reports/`](reports/), and the
analysis is in [`REPORT.md`](REPORT.md).

## Setup instructions

```bash
cd students/yair91/homework-3
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pre-commit install
```

## Pre-commit hooks configured

Fourteen hook entries across six repositories. They run in this order so the
formatters finish before the linters look at the result.

| Hook | What it stops |
| --- | --- |
| `trailing-whitespace` | Invisible characters at the end of a line |
| `end-of-file-fixer` | Files without a final newline |
| `check-yaml` | A YAML file that does not parse |
| `check-json` | A JSON file that does not parse |
| `check-toml` | A TOML file that does not parse |
| `check-added-large-files` | Anything over 500 KB |
| `check-merge-conflict` | Conflict markers left in the code |
| `detect-private-key` | A key committed by accident |
| `mixed-line-ending` | CRLF sneaking into the repository |
| `black` | Inconsistent formatting |
| `isort` | Imports out of order |
| `pylint` | Everything in `.pylintrc`, over `src/` |
| `bandit` | Known insecure patterns, over `src/` |
| `conventional-pre-commit` | A commit message off format |

Running them:

```bash
pre-commit run --all-files
```

> One caution learned the hard way: `--all-files` means every file in the
> **git repository**, not every file in the current folder. In this course
> repo that reaches everyone else's submissions. To check only this project,
> use `pre-commit run --files src/*.py`. Day to day the hooks only see staged
> files, so this is a concern for manual runs, not for committing.

## Linting

```bash
# Lint
pylint --rcfile=.pylintrc src/

# Format and sort imports
black --line-length=120 src/
isort --profile=black --line-length=120 src/

# Security scan
bandit -c bandit.yaml -r src/
```

Configuration lives in three files: `.pylintrc` for pylint, `pyproject.toml`
for black and isort, and `bandit.yaml` for bandit.

`.pylintrc` disables nothing. The only relaxed setting is
`min-public-methods = 1`, with the reason written next to it: `Product` and
`Movement` are value objects, and forcing a second public method on them would
move logic into the wrong class.

## Project structure

```
homework-3/
├── src/
│   ├── __init__.py
│   ├── inventory.py             catalogue and stock levels
│   ├── movements.py             stock in and out, with a log
│   └── reports.py               low stock, valuation, CSV export
├── reports/
│   ├── pylint-before.txt        6.10/10, 48 findings
│   ├── pylint-after.txt         10.00/10
│   ├── bandit-after.txt         0 issues
│   └── pre-commit-run.txt       all hooks passing
├── ci/
│   └── static-analysis.yml      CI workflow (bonus)
├── .pre-commit-config.yaml
├── .pylintrc
├── pyproject.toml               black and isort
├── bandit.yaml
├── example.json                 sample catalogue, also gives check-json work
├── README.md
├── REPORT.md                    the analysis (Part 6)
├── STYLE_GUIDE.md               team style guide (bonus)
└── requirements.txt
```

## What was tested

Nothing, deliberately. This is the static testing module: the tools read the
code without running it. The project has no test suite and the grading for
this homework weighs structure at 75 % and linting at 25 %, with no points for
tests or coverage.

That said, the code does work. It can be exercised by hand:

```python
from src.inventory import Inventory
from src.reports import low_stock_report

inventory = Inventory()
inventory.load_from_json("example.json")
print(low_stock_report(inventory))
# GAD-002: 3 units left (reorder point 5)
# BRK-004: 2 units left (reorder point 5)
```

## Bonus work

- **Security linting** — bandit, configured in `bandit.yaml` and wired into
  the pre-commit hooks. Reports 0 issues.
- **Team style guide** — [`STYLE_GUIDE.md`](STYLE_GUIDE.md).
- **CI for static analysis** — [`ci/static-analysis.yml`](ci/static-analysis.yml).
  It is under `ci/` rather than `.github/workflows/` because GitHub only reads
  workflows from the repository root, and this project lives in a
  subdirectory; placing it there would run against the entire course repo. In
  a standalone repository the file goes to
  `.github/workflows/static-analysis.yml` unchanged.
