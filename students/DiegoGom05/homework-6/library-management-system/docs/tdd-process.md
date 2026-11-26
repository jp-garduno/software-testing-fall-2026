# TDD Process Documentation

This document describes 5 complete Red-Green-Refactor cycles from the
development of the Library Management System.

---

## Cycle #1: Book Availability Check

### RED Phase

**Test Written**:

```python
def test_book_not_available_when_no_copies():
    book = Book("1234567890", "Test Book", "Author", copies=0)
    assert book.is_available() is False
```

**Test Result**: FAIL - `assert True is False`. A previous test had forced
`is_available()` to exist, but I had implemented it as `return True`, the
simplest code that passed that earlier test.

### GREEN Phase

**Code Written**:

```python
def is_available(self):
    return self.available_copies > 0
```

**Test Result**: PASS - all tests green.

### REFACTOR Phase

**Improvements Made**: Extracted the repeated `Book(...)` construction in the
tests into a pytest fixture.

**Design Decision**: `is_available()` returns a boolean, not a count, so the
API reads naturally (`if book.is_available():`) and callers never compare numbers.

---

## Cycle #2: ISBN Validation (incremental growth)

### RED Phase

**Test Written** (3 consecutive mini-cycles):

```python
def test_isbn_rejects_invalid_length():
    with pytest.raises(ValueError):
        Book("123456789", "T", "A")

def test_isbn_accepts_13_digits():
    assert Book("1234567890123", "T", "A").isbn == "1234567890123"

def test_isbn_rejects_non_digits():
    with pytest.raises(ValueError):
        Book("12345abcde", "T", "A")
```

**Test Result**:

- 1st: FAIL - `DID NOT RAISE <class 'ValueError'>`
- 2nd: FAIL - `ValueError: ISBN must be 10 or 13 digits` (my first
  implementation only accepted length 10)
- 3rd: FAIL - `DID NOT RAISE` (10 characters with letters passed)

### GREEN Phase

**Code Written** (final state after the 3 cycles):

```python
if not isbn.isdigit() or len(isbn) not in (10, 13):
    raise ValueError("ISBN must be 10 or 13 digits")
```

**Test Result**: PASS - all tests green.

### REFACTOR Phase

**Improvements Made**:

```python
class Book:
    VALID_ISBN_LENGTHS = (10, 13)

    @classmethod
    def _validate_isbn(cls, isbn):
        if not isbn.isdigit() or len(isbn) not in cls.VALID_ISBN_LENGTHS:
            raise ValueError("ISBN must be 10 or 13 digits")
```

**Design Decision**: The validation grew one test at a time and I only
extracted it once the rule was complete. This removed the magic numbers and
kept `__init__` readable.

---

## Cycle #3: Member Borrow Limit

### RED Phase

**Test Written**:

```python
def test_cannot_borrow_when_limit_reached():
    m = Member("m1", "Ana", max_borrow_limit=1)
    m.add_borrowed_book("1234567890")
    assert m.can_borrow() is False
```

**Test Result**: FAIL - `assert True is False`, because `can_borrow()` was
still hardcoded to `return True`.

### GREEN Phase

**Code Written**:

```python
def can_borrow(self):
    return len(self.borrowed_books) < self.max_borrow_limit
```

A second test (`test_add_borrowed_book_raises_over_limit`) then drove this:

```python
def add_borrowed_book(self, isbn):
    if not self.can_borrow():
        raise ValueError("Borrow limit reached")
    self.borrowed_books.append(isbn)
```

**Test Result**: PASS - all tests green.

### REFACTOR Phase

**Improvements Made**: None needed. `add_borrowed_book` reuses `can_borrow()`
so the limit rule lives in one place.

**Design Decision**: The limit is enforced inside `Member`, not only in
`Library`. The object protects its own invariant, so no caller can bypass it.

---

## Cycle #4: Borrowing at the Limit (a test that found a bug)

### RED Phase

**Test Written**:

```python
def test_borrow_at_member_limit_fails_and_keeps_copies(library):
    b1, b2 = make_book("1234567890"), make_book("1234567891", copies=2)
    library.add_book(b1)
    library.add_book(b2)
    library.register_member(Member("m1", "Ana", max_borrow_limit=1))
    library.borrow_book("m1", "1234567890")
    with pytest.raises(ValueError):
        library.borrow_book("m1", "1234567891")
    assert b2.available_copies == 2
```

**Test Result**: FAIL - `assert 1 == 2`. The exception was raised, but the
book had already lost a copy.

### GREEN Phase

**Code Written**:

```python
if not member.can_borrow():
    raise ValueError("Member reached borrow limit")
book.borrow()
member.add_borrowed_book(isbn)
```

**Test Result**: PASS - all tests green.

### REFACTOR Phase

**Improvements Made**: `borrow_book`, `return_book` and `get_member` all
repeated the "exists or raise" checks, so I extracted:

```python
def _find_member(self, member_id):
    if member_id not in self._members:
        raise ValueError("Member not found")
    return self._members[member_id]

def _find_book(self, isbn):
    if isbn not in self._books:
        raise ValueError("Book not found")
    return self._books[isbn]
```

**Design Decision**: Validate everything first, then mutate state. A failed
operation must leave the system unchanged. The test caught an ordering bug I
would not have noticed by reading the code.

---

## Cycle #5: Late Fees with Injected Dates

### RED Phase

**Test Written**:

```python
def test_late_fee_is_one_dollar_per_overdue_day(loaded):
    lib, _, _ = loaded
    lib.borrow_book("m1", "1234567890", borrow_date=date(2026, 1, 1))
    assert lib.calculate_late_fees("m1", today=date(2026, 1, 20)) == 5
```

**Test Result**: FAIL - `assert 0 == 5`, because `calculate_late_fees` was a
stub returning 0. Earlier, the `borrow_date` parameter had already been
introduced by a failing test (`TypeError: unexpected keyword argument`).

### GREEN Phase

**Code Written**:

```python
def calculate_late_fees(self, member_id, today=None):
    today = today or date.today()
    total = 0
    for borrowed_on in self._loans.values():
        due = borrowed_on + timedelta(days=14)
        days_late = (today - due).days
        if days_late > 0:
            total += days_late
    return total
```

**Test Result**: PASS. The next test (`test_returned_book_has_no_late_fee`)
failed with `assert 17 == 0`, which revealed that returned loans were never
removed. I fixed it with `del self._loans[(member_id, isbn)]` in `return_book`.

### REFACTOR Phase

**Improvements Made**:

```python
LOAN_PERIOD_DAYS = 14

@classmethod
def _due_date(cls, borrowed_on):
    return borrowed_on + timedelta(days=cls.LOAN_PERIOD_DAYS)
```

**Design Decision**: Dates are injectable (`borrow_date`, `today`) with
`date.today()` only as a default. This keeps tests deterministic and fast
without mocking the clock. The design came directly from the difficulty of
writing the test.
