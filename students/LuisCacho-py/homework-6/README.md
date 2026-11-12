# Library Management System (Homework 6 - TDD)

A modular **Library Management System** built using **strict Test Driven Development (TDD)** following the **Red-Green-Refactor** cycle in Python.

---

## 📋 Features

### Core Domain (Part 1)
- **Book Management**: ISBN validation (10 or 13 digits), title/author validation, copy availability tracking (`borrow`, `return_copy`, `is_available`).
- **Member Management**: ID and name validation, configurable borrow limit (default 3), loan capacity tracking (`can_borrow`, `add_borrowed_book`, `return_book`).
- **Library Coordinator**: Catalog operations (`add_book`, `get_book`), member registration (`register_member`, `get_member`), loan orchestration (`borrow_book`, `return_book`), case-insensitive search (`search_by_title`, `search_by_author`), and availability query (`get_available_books`).

### Advanced Features (Part 3)
1. **Late Fee Calculation System**:
   - $1 per day overdue assessment on loans returned past the 14-day loan window.
   - Dynamic real-time calculation of member outstanding balances across active overdue loans and unpaid returns (`get_member_total_late_fees`).
   - Fee payment processing with balance tracking and validation (`pay_late_fee`).
2. **Borrowing History & Analytics**:
   - Complete historical tracking of active and returned loans per member (`get_member_history`).
   - Catalog popularity analytics returning the most borrowed books sorted by frequency (`get_most_borrowed_books`).
3. **Book Reservation System**:
   - First-In-First-Out (FIFO) queue for reserving unavailable books (`reserve_book`).
   - Precondition checks preventing reservations on available books or duplicate requests.
   - Queue inspection (`get_next_reservation`, `get_reservations`) and cancellation management (`cancel_reservation`).

---

## 🛠️ Project Structure

```text
homework-6/
├── README.md               # Project documentation and test guides
├── pyproject.toml          # Project configuration and tool settings
├── requirements.txt        # Python dependency manifest
├── .gitignore              # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── book.py             # Book domain entity
│   ├── member.py           # Member domain entity
│   └── library.py          # Library service, Loan entity, and business logic
├── tests/
│   ├── __init__.py
│   ├── test_book.py        # TDD unit tests for Book
│   ├── test_member.py      # TDD unit tests for Member
│   └── test_library.py     # TDD unit tests for Library and advanced features
├── docs/
│   ├── tdd-process.md      # Part 2: 5 documented Red-Green-Refactor cycles
│   └── reflection.md       # Part 5: 500-700 word TDD reflection essay
└── coverage/               # Part 4: HTML coverage reports
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+ (Tested with Python 3.14)
- `pip` package manager

### Environment Setup
1. Clone or navigate to the project directory:
   ```bash
   cd students/LuisCacho-py/homework-6
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 Running Tests & Coverage

### Run All Tests
Execute pytest to run the complete test suite:
```bash
pytest
```

### Run Tests with Real-Time Terminal & HTML Coverage
Run the full test suite and regenerate the HTML report:
```bash
pytest --cov=src --cov-report=term-missing --cov-branch --cov-report=html:coverage
```

### View Coverage Report in Browser
Open the HTML coverage report:
- **Windows**:
  ```powershell
  start coverage/index.html
  ```
- **macOS / Linux**:
  ```bash
  open coverage/index.html
  ```

---

## 📊 Quality & Performance Metrics
- **Tests**: 54 passing tests.
- **Speed**: Full test execution takes **< 0.3 seconds** (well within the 2.0s limit).
- **Statement Coverage**: **99%** (exceeds the 90% rubric threshold).
- **Branch Coverage**: **94%** (exceeds the 85% rubric threshold).
- **Commit History**: 40+ granular Git commits adhering to `RED:`, `GREEN:`, and `REFACTOR:` conventions.
