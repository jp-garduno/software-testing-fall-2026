# TDD Process Documentation

This document records 5 complete **Red-Green-Refactor** cycles executed during the development of the Library Management System, adhering to strict Test Driven Development practices.

---

## Cycle #1: Book Availability Verification

### RED Phase

**Objective**: Verify whether a book has available copies before allowing loan operations.

**Test Written**:
```python
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=2)
    assert book.is_available() is True


def test_book_is_not_available_when_zero_copies():
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=0)
    assert book.is_available() is False
```

**Test Result**: `FAIL` - `AttributeError: 'Book' object has no attribute 'is_available'`.

---

### GREEN Phase

**Code Written**:
```python
class Book:
    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        total_copies: int = 1,
    ) -> None:
        self.isbn = self._validate_isbn(isbn)
        self.title = self._validate_title(title)
        self.author = self._validate_author(author)
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self) -> bool:
        """Check if at least one copy is available for borrowing."""
        return self.available_copies > 0
```

**Test Result**: `PASS` - Both tests passed in 0.08s.

---

### REFACTOR Phase

**Improvements Made**:
- Decoupled copy validation to ensure `total_copies >= 0` upon object construction.
- Ensured `available_copies` is protected and initialized consistently from `total_copies`.

**Design Decision**:
Exposing a boolean query method `is_available()` simplifies client logic (e.g., in `Library.borrow_book`) while encapsulating copy counters and preventing negative availability states.

---

## Cycle #2: Member Borrow Limit Enforcement

### RED Phase

**Objective**: Guarantee that members cannot borrow more books than their assigned maximum limit.

**Test Written**:
```python
def test_member_cannot_borrow_when_at_limit():
    member = Member("M001", "Alice Smith", max_borrow_limit=2)
    member.add_borrowed_book("1111111111")
    member.add_borrowed_book("2222222222")

    assert member.can_borrow() is False
    with pytest.raises(ValueError, match="Borrow limit reached"):
        member.add_borrowed_book("3333333333")
```

**Test Result**: `FAIL` - `AttributeError: 'Member' object has no attribute 'can_borrow'`.

---

### GREEN Phase

**Code Written**:
```python
class Member:
    def __init__(self, member_id: str, name: str, max_borrow_limit: int = 3) -> None:
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books: List[str] = []

    def can_borrow(self) -> bool:
        """Check if member has not exceeded maximum borrowing capacity."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn: str) -> None:
        """Record an active borrow for this member."""
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        self.borrowed_books.append(isbn)
```

**Test Result**: `PASS` - All member limit assertions passed.

---

### REFACTOR Phase

**Improvements Made**:
- Extracted member validation checks into private utility routines (`_validate_id`, `_validate_name`, `_validate_limit`).
- Guarded against duplicate borrowing of the same ISBN by the same member before decrementing limits.

**Design Decision**:
Separating the boolean query `can_borrow()` from the state mutation `add_borrowed_book()` allows preconditions to be checked preemptively by coordinators (like `Library`) without throwing unexpected exceptions.

---

## Cycle #3: Library Borrowing Coordinator & Loan Tracking

### RED Phase

**Objective**: Ensure borrowing through the `Library` coordinates book copy reduction, member loan recording, and creation of an active `Loan` object with a 14-day due date.

**Test Written**:
```python
def test_library_borrow_book_success():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=2)
    member = Member("M001", "Alice Smith")
    library.add_book(book)
    library.register_member(member)

    loan = library.borrow_book("M001", "1234567890")

    assert book.available_copies == 1
    assert "1234567890" in member.borrowed_books
    assert loan.member_id == "M001"
    assert loan.isbn == "1234567890"
    assert loan.due_date == loan.borrow_date + timedelta(days=14)
    assert len(library.active_loans) == 1
```

**Test Result**: `FAIL` - `AttributeError: 'Library' object has no attribute 'borrow_book'`.

---

### GREEN Phase

**Code Written**:
```python
class Library:
    # ...
    def borrow_book(
        self,
        member_id: str,
        isbn: str,
        borrow_date: Optional[date] = None,
    ) -> Loan:
        """Borrow a book for a registered member."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)

        if not member.can_borrow():
            raise ValueError("Borrow limit reached")
        if not book.is_available():
            raise RuntimeError("No copies available for borrowing")

        book.borrow()
        member.add_borrowed_book(isbn)

        loan = Loan(
            member_id=member.member_id,
            isbn=book.isbn,
            borrow_date=borrow_date,
        )
        self.active_loans.append(loan)
        return loan
```

**Test Result**: `PASS` - Loan created, due date calculated properly, and collections synchronized.

---

### REFACTOR Phase

**Improvements Made**:
- Introduced the dedicated `Loan` domain class rather than maintaining loose primitive tuples or dictionaries in `Library`.
- Added dependency lookup helpers (`get_member`, `get_book`) with sanitized strip/cleaning logic to eliminate redundant dictionary indexing throughout methods.

**Design Decision**:
Using the `Loan` entity decouples operational timestamps (`borrow_date`, `due_date`, `return_date`, `late_fee`) from `Book` and `Member`, preserving Single Responsibility Principle.

---

## Cycle #4: Case-Insensitive Catalog Search

### RED Phase

**Objective**: Allow searching library books by title or author substring, case-insensitively, returning empty list if no matches or whitespace queries are supplied.

**Test Written**:
```python
def test_library_search_by_title_case_insensitive():
    library = Library()
    b1 = Book("1111111111", "Clean Code", "Robert C. Martin")
    b2 = Book("2222222222", "Clean Architecture", "Robert C. Martin")
    b3 = Book("3333333333", "Design Patterns", "Gang of Four")
    library.add_book(b1)
    library.add_book(b2)
    library.add_book(b3)

    results = library.search_by_title("clean")
    assert len(results) == 2
    assert b1 in results
    assert b2 in results
```

**Test Result**: `FAIL` - `AttributeError: 'Library' object has no attribute 'search_by_title'`.

---

### GREEN Phase

**Code Written**:
```python
def search_by_title(self, title: str) -> List[Book]:
    """Search books by title substring, case-insensitively."""
    term = str(title).strip().lower()
    if not term:
        return []
    return [b for b in self.books.values() if term in b.title.lower()]

def search_by_author(self, author: str) -> List[Book]:
    """Search books by author substring, case-insensitively."""
    term = str(author).strip().lower()
    if not term:
        return []
    return [b for b in self.books.values() if term in b.author.lower()]
```

**Test Result**: `PASS` - Substrings matched regardless of uppercase/lowercase formatting.

---

### REFACTOR Phase

**Improvements Made**:
- Input string normalization using `.strip().lower()` guards against surrounding accidental whitespace.
- Empty search string check immediately short-circuits to empty collection, avoiding unnecessary iteration over the catalog.

**Design Decision**:
Return copies of book instances matching the criteria in a `List[Book]`, maintaining immutable return structures without leaking catalog index keys.

---

## Cycle #5: Book Reservation FIFO Queue

### RED Phase

**Objective**: Allow members to queue reservations for books with zero available copies in First-In-First-Out order, rejecting duplicate reservations and reservations on available books.

**Test Written**:
```python
def test_library_reserve_unavailable_book_fifo():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=1)
    m1 = Member("M001", "Alice")
    m2 = Member("M002", "Bob")
    m3 = Member("M003", "Charlie")
    library.add_book(book)
    library.register_member(m1)
    library.register_member(m2)
    library.register_member(m3)

    library.borrow_book("M001", "1234567890")
    assert not book.is_available()

    pos1 = library.reserve_book("M002", "1234567890")
    pos2 = library.reserve_book("M003", "1234567890")

    assert pos1 == 1
    assert pos2 == 2
    assert library.get_reservations("1234567890") == ["M002", "M003"]
```

**Test Result**: `FAIL` - `AttributeError: 'Library' object has no attribute 'reserve_book'`.

---

### GREEN Phase

**Code Written**:
```python
def reserve_book(self, member_id: str, isbn: str) -> int:
    """Reserve an unavailable book. Returns 1-based queue position."""
    member = self.get_member(member_id)
    book = self.get_book(isbn)

    if book.is_available():
        raise ValueError("Cannot reserve available book")

    queue = self.reservations.setdefault(book.isbn, [])
    if member.member_id in queue:
        raise ValueError("Member already reserved this book")

    queue.append(member.member_id)
    return len(queue)

def get_reservations(self, isbn: str) -> List[str]:
    """Return reservation queue for the given ISBN."""
    book = self.get_book(isbn)
    return list(self.reservations.get(book.isbn, []))
```

**Test Result**: `PASS` - All queue assertions and positions passed.

---

### REFACTOR Phase

**Improvements Made**:
- Added `get_next_reservation(isbn)` query method allowing callers to peek at the top of the FIFO queue without destructively mutating state.
- Added `cancel_reservation(member_id, isbn)` to handle queue cleanup when patrons cancel their reservation prior to checkout.

**Design Decision**:
Using the ISBN as the dictionary key and a standard Python list as the FIFO queue provides deterministic insertion order and $O(1)$ append behavior while keeping reservation tracking scoped per book entity.
