# Homework 6: TDD Feature Development — Library Management System

**Student**: Pablo Portillo
**Module**: 6 — Test Driven Development

## Description

A library management system built twice with strict Test Driven Development, once in Python and once in
JavaScript, following [homework-6.md](../../../06-test-driven-development/homework/homework-6.md). Every
behaviour started as a failing test committed on its own (`RED`), then the least code that made it pass
(`GREEN`), then cleanup with the suite still green (`REFACTOR`).

| | Python | JavaScript |
| --- | --- | --- |
| Tests | 77 passed | 71 passed |
| Statement coverage | 100% | 100% |
| Branch coverage | 100% | 100% |
| Suite run time | ~0.3 s | ~0.6 s |
| Static analysis | pylint 10.00/10 | ESLint: 0 errors |

All five advanced features from Part 3 are implemented in both languages (bonus).

## Prerequisites

- Python 3.11+ with pytest and pytest-cov (`requirements.txt`)
- Node.js 22+ with Jest (`package.json`)

## Installation

```bash
# From this directory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
npm install
```

## Running the Tests

```bash
# Python
python -m pytest -v

# JavaScript
npm test
```

## Coverage Reports

```bash
# Python: terminal report, then HTML in htmlcov/index.html
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html

# JavaScript: terminal report, then HTML in coverage/index.html
npm test -- --coverage
```

`htmlcov/` and `coverage/` are regenerated on every run and ignored by git. The committed evidence is in
[docs/coverage/](docs/coverage/): the terminal output of both runs and screenshots of both HTML reports.
The grading workflow lints every `.js` file in the submission, and committing the HTML reports would add
the report's own JavaScript assets to that lint.

## Project Structure

```
homework-6/
├── src/                      # Python implementation
│   ├── book.py               # Book, BookDetails (genre, year, rating)
│   ├── member.py             # Member, MemberCategory (student, faculty, public)
│   ├── loan.py               # Loan: due date and overdue days
│   └── library.py            # Library: catalog, loans, fees, reservations, search, history
├── tests/                    # pytest suite, one file per feature
│   ├── conftest.py           # FakeClock fixture
│   ├── test_book.py
│   ├── test_member.py
│   ├── test_library.py
│   ├── test_late_fees.py
│   ├── test_reservations.py
│   ├── test_search_filters.py
│   └── test_history.py
├── js/
│   ├── src/                  # JavaScript implementation, same design
│   └── tests/                # Jest suite, same structure; fakeClock.js helper
├── docs/
│   ├── tdd-process.md        # Part 2: five Red-Green-Refactor cycles in detail
│   ├── reflection.md         # Part 5: reflection essay
│   └── coverage/             # Part 4: coverage output and HTML report screenshots
├── package.json              # Jest configuration
├── pytest.ini
└── requirements.txt
```

## Features

### Core (Part 1)

- **Book**: ISBN of 10 or 13 digits, required title, total and available copies, `is_available()`,
  `borrow()`, `return_copy()`.
- **Member**: id, name, borrowed books, borrow limit (3 by default); `can_borrow()`,
  `add_borrowed_book()`, `return_book()`; a book cannot be borrowed twice or beyond the limit.
- **Library**: `add_book`, `register_member`, `borrow_book`, `return_book`, `search_by_title`,
  `search_by_author` (partial, case-insensitive) and `get_available_books`. A borrow that fails changes
  neither the book nor the member.

### Advanced (Part 3, all five)

1. **Late fees**: loans are due 14 days after borrowing; the fee counts each day overdue up to the return
   date (or today, if the book is still out); `calculate_late_fees(member_id)` adds up a member's loans.
2. **Reservations**: a book with no copy left can be reserved; the queue is first come, first served; a
   returned copy is held for the next member in line, who is notified through an injected notifier, and the
   hold ends when they borrow it.
3. **Search with filters**: `search(genre=, year=, min_rating=, sort_by=)` combines filters with AND and
   sorts by title (default), year (oldest first) or rating (best first); missing years or ratings go last.
4. **Borrowing history**: `member_history(member_id)`, `most_borrowed_book()` (ties go to the first title
   alphabetically) and `borrow_statistics()`.
5. **Member categories**: student (limit 3, $1.00/day), faculty (limit 5, $0.50/day) and public
   (limit 2, $1.50/day). Fees are stored in cents to avoid floating-point rounding.

JavaScript uses the same design with camelCase names (`borrowBook`, `calculateLateFees`, ...),
`NotFoundError` for unknown ids, and private class fields for the library's state.

## TDD Commit History

Commits use Conventional Commits with the phase in the subject, because the repository's commit-msg hook
only accepts Conventional Commits:

```
test(homework-6): RED should stop the fee from growing after the book is returned
feat(homework-6): GREEN measure overdue days up to the return date
refactor(homework-6): REFACTOR move overdue day counting into the loan
```

The TDD history has 290 commits: 135 RED, 135 GREEN and 18 REFACTOR, plus a scaffold commit and one test commit
for two cases that passed without new code. Each RED step was committed only after the suite actually
failed, and each GREEN or REFACTOR step only after it passed.

## Author

Pablo Portillo — Software Testing, Fall 2026
