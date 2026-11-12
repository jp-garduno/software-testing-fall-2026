# Library Management System (TDD) - Homework 6

**Student**: Jorge Moreno (`Frijol75`)  
**Course**: Software Testing & Quality Assurance - Fall 2026  
**Module**: 06 - Test-Driven Development (TDD)  

---

## 📖 Overview

The **Library Management System** is a robust, modular system developed strictly adhering to the **Red-Green-Refactor** discipline of Test-Driven Development. Every feature, boundary validation, and domain rule was designed and verified through tests prior to writing any production code.

### Highlights

- **Strict TDD Methodology**: Over 30 git commits tracking RED, GREEN, and REFACTOR cycles.
- **Full Core Implementation (Part 1)**: Complete `Book`, `Member`, and `Library` modules.
- **5 Advanced Features (Part 3 + Bonus)**:
  1. *Late Fee Calculation*: Configurable daily rates, 14-day loan terms, cumulative fee tracking.
  2. *Book Reservation System*: FIFO waitlist queue, automatic notification/fulfillment on returns, cancellation support.
  3. *Multi-Filter Search & Sorting*: Filtering by genre, publication year range, and minimum rating with AND logic, plus ascending/descending sorting by title, year, and rating.
  4. *Borrowing History & Statistics*: Comprehensive per-member borrowing history logs, active loans tracking, and library-wide analytics (most borrowed book).
  5. *Member Categories*: Student (3 books, $0.50/day), Faculty (5 books, $0.25/day), and Public (2 books, $1.00/day) with automatic limits and rate resolution.
- **100% Test Coverage (Part 4)**: 100% statement coverage and 100% branch coverage across all modules.
- **Execution Speed**: 83 independent tests run in under **0.15 seconds**.

---

## 📂 Project Structure

```
students/Frijol75/homework-6/
├── README.md                           # Documentation, setup, and test instructions
├── requirements.txt                     # Test and coverage dependencies
├── pytest.ini                          # Pytest configuration with coverage flags
├── .gitignore                          # Ignores bytecode, caches, and coverage artifacts
├── src/
│   ├── __init__.py                     # Package marker
│   ├── book.py                         # Book entity with ISBN and copy management
│   ├── member.py                       # Member entity with categories and limits
│   ├── library.py                      # Catalog coordinator and transaction manager
│   ├── loan.py                         # LoanRecord model and late fee calculation
│   └── reservation.py                  # Reservation model and FIFO queue manager
├── tests/
│   ├── __init__.py                     # Test package marker
│   ├── test_book.py                    # Unit tests for Book (14 tests)
│   ├── test_member.py                  # Unit tests for Member (15 tests)
│   ├── test_library.py                 # Core tests for Library (20 tests)
│   ├── test_late_fees.py               # Tests for late fees (6 tests)
│   ├── test_reservations.py            # Tests for reservation FIFO queue (6 tests)
│   ├── test_search_filters.py          # Tests for multi-attribute search & sorting (8 tests)
│   ├── test_history_and_stats.py       # Tests for borrowing history & analytics (4 tests)
│   ├── test_member_categories.py       # Tests for member category rates & limits (3 tests)
│   └── test_coverage_edge_cases.py     # Boundary condition & edge case tests (7 tests)
├── docs/
│   ├── tdd-process.md                  # Part 2: 5 complete Red-Green-Refactor cycles
│   └── reflection.md                   # Part 5: 500-700 word TDD reflection essay
└── coverage/                           # Generated HTML coverage reports
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (tested on Python 3.14)
- `pytest` and `pytest-cov`

### Installation

From the project root:

```bash
cd students/Frijol75/homework-6
pip install -r requirements.txt
```

---

## 🧪 Running Tests & Coverage

### 1. Run all tests with coverage report

```bash
pytest
```

Output includes detailed terminal table and exports HTML report to `coverage/index.html`.

### 2. Run a specific test suite

```bash
pytest tests/test_book.py
pytest tests/test_library.py
pytest tests/test_reservations.py
```

### 3. Generate and view HTML Coverage Report

```bash
pytest --cov=src --cov-report=html:coverage --cov-branch
open coverage/index.html
```

---

## 📊 Test Coverage Summary

```
Name                 Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------
src/__init__.py          0      0      0      0   100%
src/book.py             44      0     12      0   100%
src/library.py         141      0     68      0   100%
src/loan.py             16      0      4      0   100%
src/member.py           55      0     20      0   100%
src/reservation.py      37      0     10      0   100%
----------------------------------------------------------------
TOTAL                  293      0    114      0   100%
```

- **Total Tests**: 83 passing tests
- **Statement Coverage**: 100%
- **Branch Coverage**: 100%
- **Suite Execution Time**: ~0.10s

---

## 📜 Documentation

- [docs/tdd-process.md](docs/tdd-process.md): Detailed logs of 5 complete Red-Green-Refactor cycles including written test snippets, failure messages, passing code implementations, and refactoring rationales.
- [docs/reflection.md](docs/reflection.md): Comprehensive reflection essay answering questions regarding design impact, challenges, benefits, test-first vs test-after comparison, future usage, and learnings.
