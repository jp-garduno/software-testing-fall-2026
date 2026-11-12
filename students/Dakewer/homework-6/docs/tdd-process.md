# TDD Process Documentation

Five complete Red-Green-Refactor cycles taken from the real git history of this
project (`git log --oneline` shows the matching `RED:` / `GREEN:` / `REFACTOR:` commits).
Failure messages below are the actual pytest output captured during development.

---

## Cycle #1: Book Availability Check ("fake it" and triangulation)

### RED Phase

**Test Written** (`tests/test_book.py`):

```python
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() is True
```

**Test Result**: FAIL - `AttributeError: 'Book' object has no attribute 'is_available'`

### GREEN Phase

**Code Written** - the simplest thing that passes (deliberately a constant):

```python
def is_available(self):
    return True
```

**Test Result**: PASS - 3 passed

### Second RED (triangulation)

A constant cannot be the final design, so a second test forces the real rule:

```python
def test_book_not_available_when_no_copies():
    book = Book("1234567890", "Test", "Author", copies=0)
    assert book.is_available() is False
```

**Test Result**: FAIL - `assert True is False` (`is_available()` returned `True`)

```python
def is_available(self):
    return self.available_copies > 0
```

**Test Result**: PASS - 4 passed

### REFACTOR Phase

**Improvements Made**: None needed at this point; the method is a single expression.

**Design Decision**: `is_available()` returns a boolean rather than exposing a count, so
callers (`Library.borrow_book`, `get_available_books`) never reimplement the rule.
`borrow()` later reuses it as its guard.

---

## Cycle #2: ISBN Validation (two tests, two rules)

### RED Phase

**Test Written**:

```python
def test_book_rejects_isbn_with_wrong_length():
    with pytest.raises(ValueError):
        Book("12345", "Test Book", "Author")
```

**Test Result**: FAIL - `Failed: DID NOT RAISE ValueError`

### GREEN Phase

**Code Written** - only the length rule, because only the length is tested:

```python
if len(isbn) not in (10, 13):
    raise ValueError("ISBN must be 10 or 13 digits")
```

**Test Result**: PASS - 6 passed

### Second RED

```python
def test_book_rejects_isbn_with_non_digits():
    with pytest.raises(ValueError):
        Book("12345abcde", "Test Book", "Author")
```

**Test Result**: FAIL - `DID NOT RAISE ValueError` (ten characters passes the length check)

```python
if len(isbn) not in (10, 13) or not isbn.isdigit():
    raise ValueError("ISBN must be 10 or 13 digits")
```

**Test Result**: PASS - 8 passed

### REFACTOR Phase

**Improvements Made**: After title and copies validation were also added to `__init__`,
the constructor mixed validation with assignment. Each rule moved to a static helper
(`_validate_isbn`, `_validate_title`, `_validate_copies`).

```python
def __init__(self, isbn, title, author, copies=1):
    self._validate_isbn(isbn)
    self._validate_title(title)
    self._validate_copies(copies)
    ...
```

**Design Decision**: The constructor now reads as a list of rules followed by plain
assignment. All 15 Book tests stayed green without modification, which confirmed the
refactor changed structure and not behaviour.

---

## Cycle #3: Member Borrow Limit

### RED Phase

**Test Written** (`tests/test_member.py`):

```python
def test_member_cannot_borrow_at_limit():
    member = Member("M001", "Alice", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    assert member.can_borrow() is False
```

**Test Result**: FAIL - `assert True is False` (`can_borrow()` was still the constant `True`
written to pass the previous test)

### GREEN Phase

**Code Written**:

```python
def can_borrow(self):
    return len(self.borrowed_books) < self.max_borrow_limit
```

**Test Result**: PASS - 21 passed

### Next RED: enforce the rule where state changes

```python
def test_add_borrowed_book_fails_beyond_limit():
    member = Member("M001", "Alice", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError):
        member.add_borrowed_book("0987654321")
```

**Test Result**: FAIL - `DID NOT RAISE ValueError`

```python
def add_borrowed_book(self, isbn):
    if not self.can_borrow():
        raise ValueError("Borrow limit reached")
    self.borrowed_books.append(isbn)
```

**Test Result**: PASS - 22 passed

### REFACTOR Phase

**Improvements Made**: Duplicate-loan, id and name checks were added in later cycles; the
identity checks were extracted into `_validate_identity`.

**Design Decision**: `add_borrowed_book` reuses `can_borrow()` instead of repeating the
comparison, so the limit rule lives in exactly one place. This paid off in the member
categories feature: only the way the limit is *chosen* changed, never how it is *checked*.

---

## Cycle #4: Atomic Borrowing in Library (a test that found a real bug)

### RED Phase

**Test Written** (`tests/test_library.py`):

```python
def test_failed_borrow_at_limit_does_not_take_a_copy(library):
    library.add_book(Book("1234567890", "A", "Author", copies=2))
    library.add_book(Book("0987654321", "B", "Author", copies=2))
    library.register_member(Member("M001", "Alice", max_borrow_limit=1))
    library.borrow_book("M001", "1234567890")
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("M001", "0987654321")
    assert library.get_book("0987654321").available_copies == 2
```

**Test Result**: FAIL - the copy count was 1 instead of 2. The first implementation called
`book.borrow()` *before* `member.add_borrowed_book()`, so when the member was at the limit
the book had already lost a copy: a bug no earlier test could see.

### GREEN Phase

**Code Written** - register the loan on the member first, so the limit check fails before
any book state changes:

```python
member.add_borrowed_book(isbn)
book.borrow()
```

**Test Result**: PASS - 35 passed

### Next RED: the opposite failure order

Reordering opened the mirror-image bug (member records a loan, then the book has no copy).
A second test (`test_failed_borrow_of_unavailable_book_leaves_member_untouched`) failed
for exactly that reason, and was fixed by checking `book.is_available()` before touching
the member.

### REFACTOR Phase

**Improvements Made**: `get_member` and `get_book` (which raise `Unknown member` / `Unknown book`)
replaced the repeated `if x not in self._...` blocks in `borrow_book` and `return_book`.

```python
member = self.get_member(member_id)
book = self.get_book(isbn)
```

**Design Decision**: The public getters double as the validation, giving one consistent
error message for every operation. Writing the tests first also made the ordering of the
operations an explicit, tested design decision rather than an accident.

---

## Cycle #5: Late Fee Calculation (feature built in small steps)

### RED Phase

**Test Written** (`tests/test_late_fees.py`):

```python
def test_late_fee_is_one_dollar_per_overdue_day(library):
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    assert library.calculate_late_fee("M001", as_of=date(2026, 1, 20)) == 5
```

**Test Result**: FAIL - `assert 0 == 5` (the previous cycle's fake `return 0`)

### GREEN Phase

**Code Written**:

```python
def calculate_late_fee(self, member_id, as_of):
    fee = 0
    for (loan_member, isbn), borrowed_on in self._loans.items():
        due = borrowed_on + timedelta(days=LOAN_DAYS)
        if loan_member == member_id and as_of > due:
            fee += (as_of - due).days
    return fee
```

**Test Result**: PASS - 47 passed

### Following RED/GREEN steps

- `should stop accruing fees once a book is returned` failed with `45 == 0`; fixed by deleting
  the loan in `return_book`.
- `should report the late fee when returning an overdue book` failed with `TypeError`
  (unknown `return_date` argument); fixed by adding `return_date` and returning the fee.

### REFACTOR Phase

**Improvements Made**: Fee arithmetic existed twice (`calculate_late_fee` and the new
per-loan fee in `return_book`). Both now use `_loan_fee`.

```python
def calculate_late_fee(self, member_id, as_of):
    return sum(
        self._loan_fee(loan_member, isbn, as_of)
        for loan_member, isbn in self._loans
        if loan_member == member_id
    )
```

**Design Decision**: Dates are injected (`borrow_date`, `return_date`, `as_of`) instead of
calling `date.today()` everywhere. Tests stay deterministic and instant, with no mocks. Having
a single `_loan_fee` made the next feature trivial: member categories only multiplied the
result by `member.late_fee_rate`, driven by one failing test.

---

## Summary

| Cycle | Technique shown | Key lesson |
| ----- | --------------- | ---------- |
| 1 | Fake it, then triangulate | A second test removes a hard-coded constant |
| 2 | One rule per test | Write only the code the failing test demands |
| 3 | Reuse a rule in one place | Small helpers keep later features cheap |
| 4 | Test discovers a real bug | Test-first exposes ordering/atomicity problems |
| 5 | Incremental feature + dependency injection | Injectable dates make time-based code easy to test |
