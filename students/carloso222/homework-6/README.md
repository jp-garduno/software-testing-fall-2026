# Homework 6: TDD Library Management System

A library management system built with Test Driven Development in Python.
Every feature was driven by a failing test first (RED), then the minimum code to
pass (GREEN), then cleanup (REFACTOR).

## Features

**Core (Part 1)**

- `Book`: ISBN (10 or 13 digits), required title, total and available copies,
  `is_available()`, `borrow()`, `return_copy()`
- `Member`: ID, name, borrowed books, borrow limit (default 3),
  `can_borrow()`, `add_borrowed_book()`, `return_book()`
- `Library`: `add_book`, `register_member`, `borrow_book`, `return_book`,
  `search_by_title`, `search_by_author`, `get_available_books`

**Advanced (Part 3, all five)**

1. **Late fees**: due 14 days after borrowing, charged per overdue day on return,
   plus fees accruing on books still out (`calculate_late_fees`, `get_overdue_loans`)
2. **Reservations**: reserve unavailable books, FIFO queue, the first in line is
   notified on return and the copy is held for them (`reserve_book`, `get_reservation_queue`)
3. **Search with filters**: genre, year, minimum rating with AND logic, sorted by
   title, author, year or rating (`search`)
4. **Borrowing history**: every loan with dates and fees, member report, most
   borrowed book (`get_member_history`, `member_history_report`, `most_borrowed_book`)
5. **Member categories**: `MemberCategory` enum

   | Category | Borrow limit | Late fee per day |
   |---|---|---|
   | Student (default) | 3 | $1.00 |
   | Faculty | 5 | $0.50 |
   | Public | 2 | $1.50 |

## Project Structure

```text
homework-6/
├── src/
│   ├── book.py
│   ├── member.py
│   ├── member_category.py
│   ├── loan.py
│   ├── library.py
│   └── exceptions.py
├── tests/
│   ├── conftest.py            # FakeClock, Mock notifier, sample library
│   ├── test_book.py
│   ├── test_member.py         # includes member categories
│   ├── test_library.py
│   ├── test_late_fees.py
│   ├── test_reservations.py
│   ├── test_search_filters.py
│   └── test_history.py
├── docs/
│   ├── tdd-process.md         # Part 2: 5 RED-GREEN-REFACTOR cycles
│   └── reflection.md          # Part 5
├── coverage/                  # HTML coverage report
├── pytest.ini
├── .coveragerc
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the Tests

```bash
pytest -v
```

## Run with Coverage

Branch coverage is enabled in `.coveragerc`, and the HTML report is written to `coverage/`.

```bash
pytest --cov --cov-report=term --cov-report=html
```

Then open `coverage/index.html`.

## Results

| Metric | Target | Result |
|---|---|---|
| Tests | 25 core + 10 advanced | 123 passing, 0 skipped |
| Statement coverage | > 90% | 100% |
| Branch coverage | > 85% | 100% |
| Suite runtime | < 2 s | ~0.4 s |

## Testing Approach

- **No real time**: `Library` takes a `clock` callable. Tests use `FakeClock`
  and call `clock.advance(days)` to make loans overdue instantly.
- **No real notifications**: `Library` takes a `notifier` callable. Tests pass a
  `unittest.mock.Mock` and assert on its calls.
- **Independent tests**: each test gets a fresh library from a fixture; no
  shared state between tests.
