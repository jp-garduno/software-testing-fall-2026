# Homework 6: Library Management System (TDD)

**Student**: Juan Pablo Gutierrez (`juanpagutierrez`)
**Module**: 6 - Test Driven Development

A library management system written in Python with strict Test Driven Development: every behavior started as a
failing test, got the smallest code that made it pass, and was then cleaned up while the suite stayed green. The git
history of this folder is the record of that process.

## Results

| Metric | Value |
| --- | --- |
| Tests | 85, all passing |
| Statement coverage | 100% (268/268) |
| Branch coverage | 100% (44/44) |
| Suite run time | ~0.2 s |
| Pylint (course config, pylint 4.1) | 10.00/10 |
| TDD commits | 159 (68 RED, 68 GREEN, 12 REFACTOR, 10 TEST) |

## Setup

Requires Python 3.11+.

```bash
cd students/juanpagutierrez/homework-6
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the tests

```bash
pytest                                                              # run the suite
pytest --cov=src --cov-branch --cov-report=term-missing              # with coverage in the terminal
pytest --cov=src --cov-branch --cov-report=html:coverage             # regenerate the HTML report
```

The committed HTML coverage report is in [`coverage/index.html`](coverage/index.html).

## Features

### Core (Part 1)

| Component | Behavior |
| --- | --- |
| `Book` | ISBN (10 or 13 digits), required title, author, `total_copies`, `available_copies`; `is_available()`, `borrow()`, `return_copy()` |
| `Member` | `member_id`, required name, `borrowed_books`, `max_borrow_limit` (default 3); `can_borrow()`, `add_borrowed_book()`, `return_book()` |
| `Library` | `add_book`, `register_member`, `borrow_book`, `return_book`, `search_by_title`, `search_by_author`, `get_available_books` |

### Advanced (Part 3): all five options

1. **Late fees** (`src/late_fees.py`, `src/loan.py`): loans are due 14 days after borrowing and cost $1 per overdue day.
   `Library.calculate_member_fees()` adds up open loans (counted to today) and returned loans (counted to the return date).
2. **Reservations** (`src/reservations.py`): you can only reserve a book with no copies on the shelf. Each book has a
   first-in, first-out waiting list. When a copy comes back, the first member in line is notified and the copy is held
   for them until they borrow it.
3. **Search with filters** (`src/search.py`): `Library.search(genre=..., publication_year=..., min_rating=...,
   sort_by=..., descending=...)`. All filters must match (AND logic). Books with no value for the sort field go last.
4. **Borrowing history** (`src/history.py`): `generate_history_report()`, `most_borrowed_book()`, `borrow_count()`.
5. **Member categories** (`MemberCategory` in `src/member.py`):

   | Category | Borrow limit | Late fee per day |
   | --- | --- | --- |
   | Student (default) | 3 | $1.00 |
   | Faculty | 5 | $0.50 |
   | Public | 2 | $1.50 |

Money uses `Decimal`, so fees are exact. Time comes from an injected `clock`, and notifications go through an injected
`notifier`. In tests both are `unittest.mock.Mock` objects, so the suite never waits, never depends on today's date and
never sends anything.

## Project structure

```
homework-6/
├── src/
│   ├── book.py            # Book, BookDetails
│   ├── member.py          # Member, MemberCategory
│   ├── library.py         # Library facade
│   ├── loan.py            # Loan record + per-loan late fee
│   ├── late_fees.py       # due dates and fee formula
│   ├── reservations.py    # ReservationDesk (queues + holds)
│   ├── history.py         # history report, most borrowed
│   ├── search.py          # SearchQuery (filters + sorting)
│   ├── exceptions.py      # LibraryError hierarchy
│   └── validation.py      # shared input checks
├── tests/                 # one test module per component/feature
├── docs/
│   ├── tdd-process.md     # Part 2: five Red-Green-Refactor cycles
│   └── reflection.md      # Part 5: reflection essay
└── coverage/              # HTML coverage report
```

## Commit conventions

- `RED: should ...`: adds one failing test. It was committed only after watching the suite fail.
- `GREEN: ...`: adds the minimum code that makes the suite pass.
- `REFACTOR: ...`: changes structure only, with the suite green before and after.
- `TEST: ...`: adds a test that passed on its first run. These document a rule that earlier code already covered. They
  are labeled separately because a test that never failed is not a RED step.
