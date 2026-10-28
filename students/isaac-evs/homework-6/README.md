# Homework 6: TDD Feature Development - Library Management System

## Description

A library management system built test-first. Every behavior began as a failing test (a `RED:` commit),
was made to pass with the smallest change (`GREEN:`), and was then cleaned up (`REFACTOR:`).
It models books, members, a library catalog with borrowing and search, and three advanced features:
late fees, member categories and book reservations.

## Prerequisites

- Python 3.11+ (also verified on Python 3.9)
- `pytest` and `pytest-cov`

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:coverage
open coverage/index.html
```

`pytest.ini` sets `pythonpath = . src`, so plain `pytest` works from this directory.

## Results

- **Tests**: 64 passing, about 0.1-0.2 s for the full suite, none skipped
- **Statement coverage**: 100% (146/146)
- **Branch coverage**: 100% (30/30)
- **Commits**: over 100: 48 RED, 48 GREEN, 12 REFACTOR, plus scaffold and documentation commits

## Project Structure

- `src/book.py` - `Book`: ISBN/title validation, copy tracking, `borrow()` / `return_copy()`
- `src/member.py` - `Member`, `MemberCategory`, `CategoryPolicy`: borrow limits and late fee rates
- `src/library.py` - `Library`: catalog, borrowing, returns, search, late fees, reservations
- `tests/` - one file per component or feature, plus `conftest.py` with a controllable `FakeClock`
- `docs/tdd-process.md` - 5 documented Red-Green-Refactor cycles
- `docs/reflection.md` - TDD reflection essay
- `coverage/` - HTML coverage report and its terminal summary

## Features

**Core (Part 1)**: books with validated ISBNs (10 or 13 digits) and titles; members with a borrow limit
(default 3); a library that adds books, registers members, borrows and returns, searches by title or
author (partial, case-insensitive) and lists available books.

**Advanced (Part 3)**, implemented with TDD:

1. **Late fees** - due 14 days after borrowing, charged per overdue day, totalled per member. The
   clock is injected, so tests move time with `FakeClock.advance(days)`.
2. **Member categories** - Student (limit 3, $1.00/day), Faculty (limit 5, $0.50/day), Public
   (limit 2, $1.50/day). The late fee rates are my own choice; the assignment only fixes the limits.
3. **Reservations** - FIFO queue per unavailable book, no duplicates, and an injected `notifier`
   called with the first reserver when the book is returned.

## Notes

- `borrow_book` and `return_book` validate before they change anything, so a failed operation leaves
  stock and member state unchanged. Tests cover each failure path.
- The reservation queue is not safe for concurrent use.
- Only the Python implementation is provided (no JavaScript bonus).
