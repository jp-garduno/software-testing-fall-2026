# TDD Process Documentation

## Introduction

This project was developed using strict **Test-Driven Development (TDD)** following the **RED → GREEN → REFACTOR** cycle:

1. **RED**: Write a small, focused automated test for a requirement that does not yet exist and observe it fail for the expected reason.
2. **GREEN**: Write the minimum production code necessary to make the failing test pass without breaking existing tests.
3. **REFACTOR**: Clean up duplication, improve naming, and refine design boundaries while keeping the entire test suite green.

Below are 5 complete Red-Green-Refactor cycles from the development of the Library Management System.

---

## Cycle #1: Book Availability Check

### RED Phase

**Test Written** (`tests/test_book.py`):

```python
def test_book_is_not_available_when_no_copies_exist():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=0,
    )

    assert book.is_available() is False
```

**Test Result**: `FAIL - AttributeError: 'Book' object has no attribute 'is_available'`

### GREEN Phase

**Code Written** (`src/book.py`):

```python
class Book:
    def __init__(self, isbn, title, author, total_copies=1, available_copies=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = (
            total_copies if available_copies is None else available_copies
        )

    def is_available(self):
        return self.available_copies > 0
```

**Test Result**: `PASS - All tests green`

### REFACTOR Phase

**Improvements Made**: Defaulted `available_copies` to `total_copies` when omitted so callers creating new catalog books do not need to repeat the copy count.

**Design Decision**: Decided to return a boolean (`self.available_copies > 0`) rather than exposing raw copy comparisons in client classes, encapsulating availability rules inside `Book`.

---

## Cycle #2: Borrowing a Book Copy and Copy-Count Invariants

### RED Phase

**Test Written** (`tests/test_book.py`):

```python
def test_borrow_raises_error_when_no_copies_are_available():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=0,
    )

    with pytest.raises(ValueError, match="No copies available"):
        book.borrow()

    assert book.available_copies == 0
```

**Test Result**: `FAIL - DID NOT RAISE <class 'ValueError'> (available_copies became -1)`

### GREEN Phase

**Code Written** (`src/book.py`):

```python
    def borrow(self):
        if self.available_copies > 0:
            self.available_copies -= 1
        else:
            raise ValueError("No copies available")
```

**Test Result**: `PASS - All tests green`

### REFACTOR Phase

**Improvements Made**: Added constructor invariants ensuring `total_copies >= 0`, `available_copies >= 0`, and `available_copies <= total_copies`, and ensured `return_copy()` never increments beyond `total_copies`.

**Design Decision**: Raising a `ValueError` directly inside `Book.borrow()` guarantees that no caller (including `Library`) can ever put a book into a negative inventory state.

---

## Cycle #3: Member Borrowing Limits and Categories

### RED Phase

**Test Written** (`tests/test_member.py`):

```python
def test_member_cannot_add_book_when_limit_is_reached():
    member = Member(
        member_id="M001",
        name="Ana",
        max_borrow_limit=1,
    )
    member.add_borrowed_book("ISBN001")

    with pytest.raises(ValueError, match="borrowing limit"):
        member.add_borrowed_book("ISBN002")

    assert member.borrowed_books == ["ISBN001"]
```

**Test Result**: `FAIL - DID NOT RAISE <class 'ValueError'>`

### GREEN Phase

**Code Written** (`src/member.py`):

```python
    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        if not self.can_borrow():
            raise ValueError("Member has reached the borrowing limit")

        self.borrowed_books.append(isbn)
```

**Test Result**: `PASS - All tests green`

### REFACTOR Phase

**Improvements Made**: Extracted `CATEGORY_CONFIG` to map member categories (`student`: 3 books / \$1.00 daily fee, `faculty`: 5 books / \$0.50 daily fee, `public`: 2 books / \$2.00 daily fee) while still allowing an explicit `max_borrow_limit` override.

**Design Decision**: Reusing `self.can_borrow()` inside `add_borrowed_book()` and `Library.borrow_book()` eliminated duplicate length comparisons and kept limit enforcement consistent across categories.

---

## Cycle #4: Overdue Late Fee Calculation

### RED Phase

**Test Written** (`tests/test_library.py`):

```python
def test_late_fee_is_one_dollar_per_day():
    library = Library()
    borrow_date = date(2026, 1, 1)
    return_date = borrow_date + timedelta(days=17)

    fee = library.calculate_late_fee(borrow_date, return_date)

    assert fee == 3
```

**Test Result**: `FAIL - AttributeError: 'Library' object has no attribute 'calculate_late_fee'`

### GREEN Phase

**Code Written** (`src/library.py`):

```python
    def calculate_late_fee(
        self, borrow_date: date, return_date: date, daily_rate: float = 1.0
    ) -> float:
        due_date = borrow_date + timedelta(days=14)
        late_days = max(0, (return_date - due_date).days)
        fee = late_days * daily_rate
        return int(fee) if fee == int(fee) else round(fee, 2)
```

**Test Result**: `PASS - All tests green`

### REFACTOR Phase

**Improvements Made**: Added `calculate_member_late_fees(member_id, loans)` which validates member existence and delegates each loan interval to `calculate_late_fee()` using the member's category-specific `late_fee_rate`.

**Design Decision**: Passing explicit `borrow_date` and `return_date` values (`datetime.date`) makes the calculation deterministic and fast without requiring `time.sleep()` or system clock patches.

---

## Cycle #5: Book Reservation Queue (FIFO) and Return Notification

### RED Phase

**Test Written** (`tests/test_library.py`):

```python
def test_returned_book_notifies_first_member_in_reservation_queue():
    library = Library()
    borrower = Member(member_id="M400", name="Current Borrower")
    member1 = Member(member_id="M401", name="First Reserver")
    member2 = Member(member_id="M402", name="Second Reserver")
    book = Book(
        isbn="1234567890",
        title="FIFO Book",
        author="Test Author",
        total_copies=1,
        available_copies=1,
    )

    library.add_book(book)
    library.register_member(borrower)
    library.register_member(member1)
    library.register_member(member2)

    library.borrow_book("M400", "1234567890")
    library.reserve_book("M401", "1234567890")
    library.reserve_book("M402", "1234567890")

    library.return_book("M400", "1234567890")

    assert len(library.notifications) == 1
    assert library.notifications[0]["member_id"] == "M401"
    assert library.reservations["1234567890"] == ["M402"]
```

**Test Result**: `FAIL - AssertionError: assert 0 == 1 (notifications list was empty)`

### GREEN Phase

**Code Written** (`src/library.py`):

```python
        if self.reservations.get(isbn):
            next_member_id = self.reservations[isbn].pop(0)
            self.notifications.append(
                {
                    "member_id": next_member_id,
                    "isbn": isbn,
                    "message": f"Book '{book.title}' ({isbn}) is now available for pickup.",
                }
            )
```

**Test Result**: `PASS - All tests green`

### REFACTOR Phase

**Improvements Made**: Consolidated reservation validation in `reserve_book()` (checking member existence, book existence, book unavailability, and duplicate reservations) and integrated notification dispatch cleanly into `return_book()`.

**Design Decision**: Using a FIFO list per ISBN (`self.reservations[isbn].pop(0)`) and recording structured notification events in `self.notifications` keeps the queue fair and easily verifiable in unit tests.
