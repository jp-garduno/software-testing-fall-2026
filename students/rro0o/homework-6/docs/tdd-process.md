# TDD Process Documentation

Five complete Red-Green-Refactor cycles taken from the real commit history of this project
(`git log --oneline` shows the matching `RED:` / `GREEN:` / `REFACTOR:` commits).

## Cycle #1: Book Availability Check

### RED Phase

**Test Written**:

```python
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() is True
```

**Test Result**: FAIL - `AttributeError: 'Book' object has no attribute 'is_available'`

### GREEN Phase

**Code Written** (a deliberate "fake it" implementation):

```python
def is_available(self):
    return True
```

**Test Result**: PASS

I then wrote a second test, `test_book_is_not_available_when_no_copies` (copies=0). It failed with
`assert True is False`, which forced the real rule:

```python
def is_available(self):
    return self.available_copies > 0
```

**Test Result**: PASS - all tests green

### REFACTOR Phase

**Improvements Made**: None needed yet; the method is one line.

**Design Decision**: `is_available()` returns a boolean instead of the number of copies, so callers
never compare counts themselves. Faking the first implementation proved that the second test was
really needed.

## Cycle #2: Borrowing Never Consumes a Copy When the Member Is Over the Limit

### RED Phase

**Test Written**:

```python
def test_borrow_over_limit_does_not_consume_a_copy():
    library = make_library()
    library.register_member(Member("m2", "Bo", max_borrow_limit=0))
    with pytest.raises(LibraryError):
        library.borrow_book("m2", ISBN)
    assert library.find_book(ISBN).available_copies == 1
```

**Test Result**: FAIL - `assert 0 == 1`. The error was raised, but only after `book.borrow()` had
already taken the copy, so the catalog became inconsistent.

### GREEN Phase

**Code Written**:

```python
if not member.can_borrow():
    raise LibraryError("Member reached the borrow limit")
book.borrow()
member.add_borrowed_book(isbn)
```

**Test Result**: PASS

### REFACTOR Phase

**Improvements Made**: Left as is; the check-then-act order is now explicit.

**Design Decision**: Validate every precondition before mutating any object. The test exposed an
ordering bug that a happy-path test would never have found.

## Cycle #3: Extracting Lookups in `Library`

### RED Phase

**Test Written**:

```python
def test_return_with_unknown_member_raises_error():
    library = make_library()
    with pytest.raises(LibraryError):
        library.return_book("nobody", ISBN)
```

**Test Result**: FAIL - `KeyError: 'nobody'` instead of `LibraryError`

### GREEN Phase

**Code Written**: an inline `if member_id not in self.members: raise LibraryError("Unknown member")`
at the top of `return_book`, duplicating the check that `borrow_book` already had.

**Test Result**: PASS

### REFACTOR Phase

**Improvements Made**: Both checks moved into two private helpers:

```python
def _require_book(self, isbn): ...
def _require_member(self, member_id): ...
```

`borrow_book`, `return_book` and later `late_fee` and `reserve_book` all reuse them.

**Design Decision**: Duplication appeared the second time the same rule was needed, so that was the
moment to extract it. The existing green tests made the change safe.

## Cycle #4: Late Fee per Member Category

### RED Phase

**Test Written**:

```python
@pytest.mark.parametrize("category,fee", [
    (MemberCategory.FACULTY, 1.5),
    (MemberCategory.PUBLIC, 4.5),
])
def test_late_fee_depends_on_member_category(category, fee):
    clock = FakeClock()
    library = make_library(clock=clock, category=category)
    library.borrow_book("m1", ISBN)
    clock.advance(17)
    assert library.late_fee("m1", ISBN) == fee
```

**Test Result**: FAIL - `assert 3 == 1.5` (every member was charged $1 per day)

### GREEN Phase

**Code Written**:

```python
rate = self._require_member(member_id).category.late_fee_rate
return max(overdue_days, 0) * rate
```

**Test Result**: PASS

### REFACTOR Phase

**Improvements Made**: Extracted `_days_overdue(member_id, isbn)` so `late_fee` reads as
"days overdue times rate".

**Design Decision**: The tests inject a `FakeClock` into `Library(clock=...)`. Testing fees made me
design the library around an injectable clock instead of calling `date.today()` directly, which keeps
the suite fast and deterministic.

## Cycle #5: Notify the First Member in the Reservation Queue

### RED Phase

**Test Written**:

```python
def test_return_notifies_the_first_member_in_line():
    library = make_busy_library()
    library.reserve_book("m2", ISBN)
    library.reserve_book("m3", ISBN)
    library.return_book("m1", ISBN)
    assert library.notifications == [("m2", ISBN)]
```

**Test Result**: FAIL - `AttributeError: 'Library' object has no attribute 'notifications'`

### GREEN Phase

**Code Written**:

```python
queue = self.reservations.get(isbn)
if queue:
    self.notifications.append((queue.pop(0), isbn))
```

**Test Result**: PASS

### REFACTOR Phase

**Improvements Made**: Moved those lines into `_notify_next_in_queue(isbn)`, so `return_book` reads
as a list of steps: validate, return the copy, notify, return the fee.

**Design Decision**: Notification is stored as data (`library.notifications`) instead of calling an
e-mail service, so the behaviour is easy to assert and the real delivery mechanism can be added later
without touching the queue logic.
