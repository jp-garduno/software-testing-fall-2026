# Homework 3: Static Testing Setup

**Student**: Rogelio Sosa
**Project**: Expense Tracker (sample library)
**Language**: Python

## Description

A small expense-tracking library with three modules: `models` (the
`Expense`/`ExpenseBook` classes), `storage` (JSON/CSV persistence), and
`reports` (aggregations such as totals, averages, and a text report
builder). It exists purely as a target for the static testing tooling in
this assignment.

## Setup Instructions

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Install the pre-commit hooks:

   ```bash
   pre-commit install --config .pre-commit-config.yaml
   ```

3. Try the library:

   ```bash
   python3 -c "
   from src.models import Expense, ExpenseBook
   from src.reports import ReportBuilder

   book = ExpenseBook()
   book.add(Expense(50, 'food', 'groceries'))
   book.add(Expense(20, 'transport', 'bus pass'))
   print(ReportBuilder(book).build())
   "
   ```

## Pre-commit Hooks Configured

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-json`
- `check-added-large-files`
- `black`
- `isort` (profile `black`)
- `pylint` (using `.pylintrc`)

## Linting

Run the linters manually with:

```bash
isort --profile=black src/
black src/
pylint --rcfile=.pylintrc src/
```

`pylint-report-before.txt` and `pylint-report-after.txt` capture the
Pylint output before and after the fixes described in `REPORT.md`.
