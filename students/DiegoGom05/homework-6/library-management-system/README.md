# Library Management System (TDD)

A Library Management System built with strict Test Driven Development
(Red-Green-Refactor) in Python.

## Features

- **Book**: ISBN validation (10/13 digits), copy tracking, borrow/return
- **Member**: borrow limits, categories (student, faculty, public)
- **Library**: catalog, member registration, borrow/return, search, availability
- **Advanced (TDD)**: member categories, late fees, borrowing history and reports

## Setup

```bash
git clone <your-repo-url>
cd library-management-system
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the tests

```bash
pytest
```

## Coverage

```bash
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

The HTML report is in `coverage/index.html`.

**Results**: <XX>% statement coverage, <XX>% branch coverage, <N> tests
passing in <X.XX> seconds.

## Project structure

```
src/        book.py, member.py, library.py
tests/      test_book.py, test_member.py, test_library.py
docs/       tdd-process.md (5 cycles), reflection.md
coverage/   HTML coverage report
```

## Late fee rules

- Loan period: 14 days
- Student: $1.00/day, Faculty: $0.50/day, Public: $1.50/day

## Git history

Commits follow the format `RED:`, `GREEN:` and `REFACTOR:`, showing the TDD
cycle for each feature.
