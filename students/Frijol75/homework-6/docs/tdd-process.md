# TDD Process Documentation: 5 Complete Red-Green-Refactor Cycles

This document records five complete Test-Driven Development (TDD) cycles implemented during the development of the **Library Management System**. Each cycle follows the strict discipline of writing failing tests first (RED), writing the minimal code to satisfy the requirements (GREEN), and refining the design and architecture with safety guarantees (REFACTOR).

---

## Cycle #1: Book Availability and Copy Bounds

### RED Phase

**Test Written**:

```python
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=2)
    assert book.is_available() is True

def test_book_is_not_available_when_copies_are_zero():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=0)
    assert book.is_available() is False

def test_book_borrow_decrements_available_copies():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=2)
    book.borrow()
    assert book.available_copies == 1

def test_book_borrow_raises_when_no_copies_available():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=1)
    book.borrow()
    with pytest.raises(ValueError, match="No copies available to borrow"):
        book.borrow()
```

**Test Result**:
`FAILED - AttributeError: 'Book' object has no attribute 'is_available'` and `'Book' object has no attribute 'borrow'`.

---

### GREEN Phase

**Code Written**:

```python
class Book:
    def __init__(self, isbn: str, title: str, author: str, total_copies: int = 1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self) -> bool:
        return self.available_copies > 0

    def borrow(self) -> None:
        if not self.is_available():
            raise ValueError("No copies available to borrow")
        self.available_copies -= 1
```

**Test Result**:
`PASS - 4 passed in 0.02s (100% test pass rate)`

---

### REFACTOR Phase

**Improvements Made**:
1. Extracted ISBN, title, and copy boundary validations into isolated static helper methods (`_validate_isbn`, `_validate_title`, `_validate_total_copies`).
2. Implemented `return_copy()` with symmetric boundary guard against returning more copies than `total_copies`.
3. Implemented `__repr__`, `__eq__`, and `__hash__` to enable value-based assertions and storage in sets and hash maps.

**Design Decision**:
Decided to store both `total_copies` and `available_copies` on `Book` as mutable state encapsulated behind `borrow()` and `return_copy()` methods, avoiding external manipulation and maintaining invariant integrity.

---

## Cycle #2: Member Borrow Limit Enforcement

### RED Phase

**Test Written**:

```python
def test_member_can_borrow_when_under_limit():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=2)
    assert member.can_borrow() is True

def test_member_cannot_borrow_when_at_limit():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=2)
    member.borrowed_books = ["1111111111", "2222222222"]
    assert member.can_borrow() is False

def test_member_add_borrowed_book_rejects_when_limit_exceeded():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=1)
    member.add_borrowed_book("1111111111")
    with pytest.raises(ValueError, match="Borrow limit reached"):
        member.add_borrowed_book("2222222222")
```

**Test Result**:
`FAILED - AttributeError: 'Member' object has no attribute 'can_borrow'`.

---

### GREEN Phase

**Code Written**:

```python
class Member:
    def __init__(self, member_id: str, name: str, max_borrow_limit: int = 3):
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []

    def can_borrow(self) -> bool:
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn: str) -> None:
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        if isbn in self.borrowed_books:
            raise ValueError("Book already borrowed by this member")
        self.borrowed_books.append(isbn)
```

**Test Result**:
`PASS - All 3 member limit tests green.`

---

### REFACTOR Phase

**Improvements Made**:
1. Added validation against empty string identifiers for both member IDs and borrowed ISBN strings.
2. Implemented `return_book(isbn)` verifying membership in the borrowed list before removal, raising descriptive `ValueError` on attempts to return unheld books.
3. Added `__repr__` detailing `Borrowed=current/max` ratio for clear debugging.

**Design Decision**:
Rather than allowing external callers to directly mutate `member.borrowed_books`, all mutations are mediated by `can_borrow()`, `add_borrowed_book()`, and `return_book()`, ensuring consistent state transitions.

---

## Cycle #3: Library Borrow and Catalog Coordination

### RED Phase

**Test Written**:

```python
def test_library_borrow_book_success():
    lib = Library()
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=2)
    member = Member("M001", "Alice")
    lib.add_book(book)
    lib.register_member(member)

    assert lib.borrow_book("M001", "1234567890") is True
    assert book.available_copies == 1
    assert "1234567890" in member.borrowed_books

def test_library_borrow_book_raises_for_unregistered_member():
    lib = Library()
    book = Book("1234567890", "Refactoring", "Martin Fowler")
    lib.add_book(book)
    with pytest.raises(KeyError, match="Member not registered"):
        lib.borrow_book("UNKNOWN", "1234567890")

def test_library_borrow_book_raises_for_missing_book():
    lib = Library()
    member = Member("M001", "Alice")
    lib.register_member(member)
    with pytest.raises(KeyError, match="Book not found in catalog"):
        lib.borrow_book("M001", "9999999999")
```

**Test Result**:
`FAILED - AttributeError: 'Library' object has no attribute 'borrow_book'`.

---

### GREEN Phase

**Code Written**:

```python
class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def borrow_book(self, member_id: str, isbn: str) -> bool:
        if member_id not in self.members:
            raise KeyError("Member not registered")
        if isbn not in self.books:
            raise KeyError("Book not found in catalog")

        member = self.members[member_id]
        book = self.books[isbn]

        if not book.is_available():
            raise ValueError("Book is not currently available")
        if not member.can_borrow():
            raise ValueError("Borrow limit reached")

        book.borrow()
        member.add_borrowed_book(isbn)
        return True
```

**Test Result**:
`PASS - All borrow coordination tests passing.`

---

### REFACTOR Phase

**Improvements Made**:
1. Added full type annotations with `Dict[str, Book]` and `Dict[str, Member]`.
2. Created audit logging by saving a structured `LoanRecord` for each borrow operation with a unique UUID, timestamp, and calculated due date (14 days default).
3. Matched `return_book()` with identical lookup guards, updating both the active loan and book availability simultaneously.

**Design Decision**:
Separated entity logic (`Book` handles stock, `Member` handles allowance) from coordination logic (`Library` verifies registration and orchestrates transactions). This adheres strictly to the Single Responsibility Principle.

---

## Cycle #4: Late Fee Calculation & Member Categories

### RED Phase

**Test Written**:

```python
def test_library_late_fees_apply_member_category_rates():
    lib = Library()
    b1 = Book("1111111111", "Faculty Book", "Author")
    b2 = Book("2222222222", "Student Book", "Author")
    b3 = Book("3333333333", "Public Book", "Author")

    faculty = Member("F001", "Dr. Smith", category=MemberCategory.FACULTY)
    student = Member("S001", "Bob Student", category=MemberCategory.STUDENT)
    public = Member("P001", "Jane Public", category=MemberCategory.PUBLIC)

    lib.add_book(b1)
    lib.add_book(b2)
    lib.add_book(b3)
    lib.register_member(faculty)
    lib.register_member(student)
    lib.register_member(public)

    borrow_date = date(2026, 10, 1)
    as_of_date = date(2026, 10, 25)  # 10 days overdue (due date Oct 15)

    lib.borrow_book("F001", "1111111111", borrow_date=borrow_date)
    lib.borrow_book("S001", "2222222222", borrow_date=borrow_date)
    lib.borrow_book("P001", "3333333333", borrow_date=borrow_date)

    assert lib.calculate_member_late_fees("F001", as_of_date=as_of_date) == 2.50   # $0.25/day
    assert lib.calculate_member_late_fees("S001", as_of_date=as_of_date) == 5.00   # $0.50/day
    assert lib.calculate_member_late_fees("P001", as_of_date=as_of_date) == 10.00  # $1.00/day
```

**Test Result**:
`FAILED - ImportError: cannot import name 'MemberCategory' from 'src.member'`.

---

### GREEN Phase

**Code Written**:

```python
class MemberCategory(str, Enum):
    STUDENT = "STUDENT"
    FACULTY = "FACULTY"
    PUBLIC = "PUBLIC"

CATEGORY_CONFIG = {
    MemberCategory.STUDENT: {"max_limit": 3, "daily_rate": 0.50},
    MemberCategory.FACULTY: {"max_limit": 5, "daily_rate": 0.25},
    MemberCategory.PUBLIC: {"max_limit": 2, "daily_rate": 1.00},
}

# In calculate_late_fee:
def calculate_late_fee(loan: LoanRecord, return_date=None, daily_rate=1.0) -> float:
    effective_return = return_date or loan.return_date or date.today()
    if loan.due_date is None or effective_return <= loan.due_date:
        return 0.0
    days_overdue = (effective_return - loan.due_date).days
    return float(days_overdue * daily_rate)
```

**Test Result**:
`PASS - All category and late fee assertions succeeded.`

---

### REFACTOR Phase

**Improvements Made**:
1. Integrated category defaults with custom parameter overrides: if a custom `max_borrow_limit` or `daily_fee_rate` is explicitly provided, it respects the override while defaulting to the category policy.
2. Stored `daily_fee_rate` directly on the `Member` object so the Library calculation dynamically uses the borrower's personalized rate.
3. Allowed string initialization for `MemberCategory` (e.g. `category="FACULTY"`) with comprehensive validation against unrecognized strings or invalid types.

**Design Decision**:
Used an Enum (`MemberCategory`) combined with a configuration dictionary (`CATEGORY_CONFIG`) instead of deep subclassing (e.g. `StudentMember`, `FacultyMember`). This prevents class explosion and allows easy runtime modification or dynamic configuration.

---

## Cycle #5: Book Reservation Queue (FIFO) and Return Notification

### RED Phase

**Test Written**:

```python
def test_reserve_book_fifo_order_and_notification_on_return():
    lib = Library()
    book = Book("1234567890", "Design Patterns", "GoF", total_copies=1)
    m1 = Member("M001", "Alice")
    m2 = Member("M002", "Bob")
    m3 = Member("M003", "Charlie")
    lib.add_book(book)
    lib.register_member(m1)
    lib.register_member(m2)
    lib.register_member(m3)

    lib.borrow_book("M001", "1234567890")
    lib.reserve_book("M002", "1234567890")
    lib.reserve_book("M003", "1234567890")

    assert lib.get_book_reservations("1234567890") == ["M002", "M003"]

    lib.return_book("M001", "1234567890")
    assert lib.get_next_reservation_notification("1234567890") == "M002"
    assert lib.get_book_reservations("1234567890") == ["M003"]
```

**Test Result**:
`FAILED - AttributeError: 'Library' object has no attribute 'reserve_book'`.

---

### GREEN Phase

**Code Written**:

```python
@dataclass
class Reservation:
    reservation_id: str
    member_id: str
    isbn: str
    status: str = "PENDING"

class ReservationManager:
    def __init__(self):
        self._queues = {}
        self._latest_notified = {}

    def add_reservation(self, res: Reservation):
        self._queues.setdefault(res.isbn, []).append(res)

    def get_queue(self, isbn: str) -> List[str]:
        return [r.member_id for r in self._queues.get(isbn, []) if r.status == "PENDING"]

    def notify_next(self, isbn: str) -> Optional[str]:
        for r in self._queues.get(isbn, []):
            if r.status == "PENDING":
                r.status = "NOTIFIED"
                self._queues[isbn].remove(r)
                self._latest_notified[isbn] = r.member_id
                return r.member_id
        return None
```

**Test Result**:
`PASS - FIFO reservation queue and return notification succeeded.`

---

### REFACTOR Phase

**Improvements Made**:
1. Encapsulated reservation logic inside a dedicated `ReservationManager` class rather than bloating `Library`.
2. Added comprehensive guards:
   - Cannot reserve a book that currently has available copies.
   - Cannot reserve a book if the member currently holds a copy.
   - Cannot create duplicate reservations for the same book by the same member.
3. Implemented `cancel_reservation(member_id, isbn)` allowing queued members to withdraw their reservation cleanly.

**Design Decision**:
Decided to store reservation queues keyed by ISBN rather than per copy. When any copy of the book is returned, the head of the FIFO queue is immediately notified, guaranteeing equitable fairness.
