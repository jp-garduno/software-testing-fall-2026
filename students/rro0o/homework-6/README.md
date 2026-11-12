# Library Management System (TDD)

Library management system built with strict Test Driven Development
(Red-Green-Refactor). Every `RED:` commit adds a failing test, the following `GREEN:`
commit makes it pass, and `REFACTOR:` commits clean up with the tests green.

## Features

- **Book**: ISBN (10/13 digits), title, author, total and available copies, borrow/return.
- **Member**: id, name, borrowed books, borrow limit (default 3).
- **Library**: catalog, member registry, borrow/return, search by title/author, available books.
- **Late fees**: due date 14 days after borrowing, charged per overdue day.
- **Member categories**: Student (3 books, $1/day), Faculty (5, $0.50/day), Public (2, $1.50/day).
- **Reservations**: FIFO queue for unavailable books, notification when a copy is returned.
- **Borrowing history**: per-member history, text report, most borrowed book.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the tests

```bash
pytest
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:coverage
```

The HTML coverage report is in `coverage/index.html` (100% statements and branches).

## Layout

```
src/        book.py, member.py, member_category.py, library.py, errors.py
tests/      test_book.py, test_member.py, test_library.py, test_late_fees.py,
            test_reservations.py, test_history.py, helpers.py
docs/       tdd-process.md (5 documented cycles), reflection.md
coverage/   HTML coverage report
```
