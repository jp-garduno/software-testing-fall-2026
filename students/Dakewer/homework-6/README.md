# Library Management System (built with strict TDD)

A small library domain model written test-first (Red-Green-Refactor) in Python.
Every feature in the git history appears as a `RED:` commit (failing test), a `GREEN:` commit
(minimum code to pass) and, when useful, a `REFACTOR:` commit.

## Features

**Core (Part 1)**

- `Book` - ISBN (10 or 13 digits), title, author, total/available copies, `borrow()`, `return_copy()`
- `Member` - id, name, borrowed books, borrow limit (default 3)
- `Library` - catalog, member registry, `borrow_book`, `return_book`, `search_by_title`,
  `search_by_author`, `get_available_books`

**Advanced (Part 3)** - three features implemented with TDD

1. **Late fees** - due date 14 days after borrowing, per-day fee for overdue books,
   total fee per member, fee reported when returning a book
2. **Member categories** - `student` (limit 3, $1.00/day), `faculty` (limit 5, $0.50/day),
   `public` (limit 2, $2.00/day)
3. **Borrowing history** - borrow/return events, member history report, most borrowed book

Dates are passed in (`borrow_date`, `return_date`, `as_of`) and default to today, so tests are
deterministic and fast.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the tests

```bash
pytest
```

## Coverage (statement + branch, HTML report)

```bash
pytest --cov=src --cov-branch --cov-report=html:coverage --cov-report=term-missing
open coverage/index.html         # Linux: xdg-open coverage/index.html
```

The generated report is committed in `coverage/`.

## Project layout

```
src/        book.py, member.py, library.py, history.py
tests/      test_book.py, test_member.py, test_library.py,
            test_late_fees.py, test_member_categories.py, test_history.py
docs/       tdd-process.md (5 documented cycles), reflection.md
coverage/   HTML coverage report
```

## Viewing the TDD history

```bash
git log --oneline --reverse
```
