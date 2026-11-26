# Library Management System — Homework 6 (TDD)

## Overview

This project implements a full **Library Management System** in Python developed strictly with **Test-Driven Development (TDD)** following the **RED → GREEN → REFACTOR** cycle.

## Implemented Features

### Part 1: Core TDD Components
- **`Book` (`src/book.py`)**: ISBN validation (10 or 13 numeric digits), non-empty title validation, copy-count invariants (`total_copies`, `available_copies`), `is_available()`, `borrow()`, and `return_copy()`.
- **`Member` (`src/member.py`)**: Member ID and name validation, `borrowed_books` tracking, `max_borrow_limit` enforcement, `can_borrow()`, `add_borrowed_book()`, and `return_book()`.
- **`Library` (`src/library.py`)**: Catalog management (`add_book`), member registration (`register_member`), borrowing/returning coordination (`borrow_book`, `return_book`), `search_by_title()`, `search_by_author()`, and `get_available_books()`.

### Part 3: Advanced Features Implemented with TDD
1. **Late Fee Calculation**: 14-day loan period, overdue calculation (`calculate_late_fee`), and aggregated member fee calculation (`calculate_member_late_fees`).
2. **Book Reservation System**: Queue-based FIFO reservations for unavailable books (`reserve_book`) and automatic notification to the first member in queue upon book return (`notifications`).
3. **Search with Filters**: Combined `AND` filtering by `genre`, `publication_year`, and `min_rating`, plus sorting by `title`, `publication_year`, or `rating` (`search_books`).
4. **Borrowing History & Statistics**: Complete audit log of borrows and returns (`borrowing_history`), per-member history (`get_member_history`), and most-borrowed book statistics (`get_most_borrowed_book`).
5. **Member Categories**: Category-specific limits and late fee rates for `student` (limit 3, \$1.00/day), `faculty` (limit 5, \$0.50/day), and `public` (limit 2, \$2.00/day).

## Project Structure

```text
homework-6/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   └── library.py
├── tests/
│   ├── __init__.py
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
├── docs/
│   ├── tdd-process.md
│   └── reflection.md
└── coverage/
    └── index.html
```

## Setup & Installation

```bash
pip install -r requirements.txt
```

## Running the Test Suite

Run all tests:

```bash
python -m pytest -v
```

Run tests with statement and branch coverage and generate the HTML report:

```bash
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:coverage
```

## Metrics Summary

- **Total Automated Tests**: 65 passing tests (`< 1.5s` execution time)
- **Statement Coverage**: 100% (`> 90%` required)
- **Branch Coverage**: 100% (`> 85%` required)
- **Pylint Score**: 10.00/10
