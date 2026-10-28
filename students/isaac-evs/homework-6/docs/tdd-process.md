# TDD Process Documentation

Every cycle below is a real sequence in the git history (`git log --oneline`). The RED output is the
actual failure pytest reported when the test was committed; a script refused to commit a `RED:`
change if the suite still passed, or a `GREEN:`/`REFACTOR:` change if it did not.

| Phase    | Commits | Meaning                                         |
| -------- | ------- | ----------------------------------------------- |
| RED      | 48      | A new test, committed while it fails            |
| GREEN    | 48      | The smallest change that makes the suite pass   |
| REFACTOR | 12      | Structure or tests improved, suite stays green  |

Six commits change more than 20 lines. They are the ones that create a test file together with
its fixtures, or that add several characterization tests in one REFACTOR commit.

---

## Cycle #1: Book availability ("fake it", then triangulate)

### RED Phase (`RED: should be available when copies exist`)

**Test Written**:

```python
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() is True
```

**Test Result**: FAIL - `AttributeError: 'Book' object has no attribute 'is_available'`

### GREEN Phase (`GREEN: fake it: is_available returns True`)

**Code Written**:

```python
    def is_available(self):
        return True
```

**Test Result**: PASS - 3 passed. A constant is enough to satisfy the only test that exists.

### Next RED (`RED: should not be available when no copies are left`)

```python
def test_book_is_not_available_when_no_copies():
    book = Book("1234567890", "Test Book", "Author", copies=0)
    assert book.is_available() is False
```

**Test Result**: FAIL - `assert True is False`. The second example is what forces real logic.

### GREEN Phase (`GREEN: is_available checks the available copies`)

```python
    def is_available(self):
        return self.available_copies > 0
```

**Test Result**: PASS - 4 passed.

### REFACTOR Phase

**Improvements Made**: None at this point; the method is one line.

**Design Decision**: `is_available()` returns a boolean rather than a count. `borrow()` and
`Library.get_available_books()` later reuse it, so the rule "available means at least one copy"
lives in exactly one place.

---

## Cycle #2: Returning a book the member never borrowed

### RED Phase (`RED: should explain why returning an unborrowed book fails`)

**Test Written**:

```python
def test_return_book_fails_when_not_borrowed():
    with pytest.raises(ValueError, match="not borrowed"):
        Member("m1", "Alice").return_book("1234567890")
```

**Test Result**: FAIL - `ValueError: list.remove(x): x not in list`. The code already raised a
`ValueError`, but Python's own message, not a domain one. The test failed for a better reason than
"nothing happens": the error was correct and unhelpful.

### GREEN Phase (`GREEN: raise a clear error when returning an unborrowed book`)

**Code Written**:

```python
    def return_book(self, isbn):
        if isbn not in self.borrowed_books:
            raise ValueError("Book not borrowed by this member")
        self.borrowed_books.remove(isbn)
```

**Test Result**: PASS - 23 passed.

### REFACTOR Phase (`REFACTOR: extract _holds helper for membership checks`)

**Improvements Made**: `isbn in self.borrowed_books` appeared in both `return_book` and
`add_borrowed_book` (the duplicate-borrow guard), so both now call a private `_holds(isbn)`.

**Design Decision**: Private, so no new test was written. It is covered through the public
behavior, which is also what made the extraction safe.

---

## Cycle #3: Borrowing must not leave the library half-updated

### RED Phase (`RED: should not take a copy when the member is at their limit`)

**Test Written**:

```python
def test_borrow_over_the_limit_does_not_take_a_copy(library):
    first = Book(ISBN, "First", "Author", copies=1)
    second = Book(OTHER_ISBN, "Second", "Author", copies=2)
    library.add_book(first)
    library.add_book(second)
    library.register_member(Member("m1", "Alice", max_borrow_limit=1))
    library.borrow_book("m1", ISBN)
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("m1", OTHER_ISBN)
    assert second.available_copies == 2
```

**Test Result**: FAIL - `assert 1 == 2`. `borrow_book` took the copy first and only then asked the
member to record it. The limit error was raised, but a copy was already gone.

### GREEN Phase (`GREEN: update the member before taking the copy`)

```python
        member.add_borrowed_book(isbn)   # may raise: limit or duplicate
        book.borrow()
```

**Test Result**: PASS - 31 passed.

### Next RED (`RED: should not record a loan for a book with no copies`)

The mirror case failed with `AssertionError: assert ['1234567890'] == []`: with the new order the
member kept a loan for a book that could not be borrowed. `GREEN: check availability before
recording the loan` added `if not book.is_available(): raise ...` before the member is touched.

### REFACTOR Phase (`REFACTOR: remove duplication between the searches and group the lookups`)

**Improvements Made**: This commit removed duplication elsewhere in `Library` (one `_search` helper
for title and author, `get_member` reusing `_require_member`). By then the two GREEN commits above had
already made `borrow_book` validate-then-act: look up member and book, check availability, record the
loan (which validates the limit), and only then take the copy. `return_book` got the same treatment
in a later cycle.

**Design Decision**: Order of operations is the transaction, since there is no database. A test
for each failure path keeps the ordering from regressing.

---

## Cycle #4: Late fees (fake it, then an invariant)

### RED Phase (`RED: should charge one dollar per overdue day`)

**Test Written**:

```python
def test_late_fee_is_one_dollar_per_overdue_day(library, clock):
    library.borrow_book("m1", ISBN)
    clock.advance(17)
    assert library.calculate_late_fee("m1", ISBN) == 3
```

**Test Result**: FAIL - `assert 0 == 3`. The previous cycle had faked `calculate_late_fee` with
`return 0`, which was enough for "no fee on the due date".

### GREEN Phase (`GREEN: charge per day past the due date`)

```python
        due = self.get_due_date(member_id, isbn)
        return max(0, (self._clock() - due).days)
```

**Test Result**: PASS - 42 passed.

### Next RED (`RED: should stop charging fees once the book is returned`)

**Test Result**: FAIL - `assert 5 == 0`. A returned book kept accruing fees because the loan record
was never removed. `GREEN: drop the loan when the book is returned` added
`del self._loans[(member_id, isbn)]`.

### REFACTOR Phase (`REFACTOR: name the loan period and fee rate and extract _overdue_days`)

**Improvements Made**: `14` became `LOAN_PERIOD_DAYS`, the fee rate became a named constant, and the
date arithmetic moved into `_overdue_days`.

**Design Decision**: The library takes an injected `clock`. The tests use a `FakeClock` with
`advance(days)`, so no test depends on today's date.

---

## Cycle #5: Member categories (design evolution)

### RED Phase (`RED: should give each member category its own borrow limit`)

**Test Written**:

```python
@pytest.mark.parametrize(
    "category, limit",
    [(MemberCategory.STUDENT, 3), (MemberCategory.FACULTY, 5), (MemberCategory.PUBLIC, 2)],
)
def test_borrow_limit_depends_on_category(category, limit):
    assert Member("m1", "Alice", category=category).max_borrow_limit == limit
```

**Test Result**: FAIL - `ImportError: cannot import name 'MemberCategory'`

### GREEN Phase (`GREEN: add MemberCategory with per-category borrow limits`)

```python
class MemberCategory(Enum):
    STUDENT = 3
    FACULTY = 5
    PUBLIC = 2
```

The enum value was only the limit, because that was all the test asked for.

### Next RED (`RED: should charge faculty half the student late fee`)

**Test Result**: FAIL - `assert 4 == 2.0`. A category now needs a second attribute.

### GREEN Phase (`GREEN: carry a late fee rate per category and use it for fees`)

```python
class MemberCategory(Enum):
    STUDENT = (3, 1.00)
    FACULTY = (5, 0.50)
    PUBLIC = (2, 1.50)
```

with `borrow_limit` / `late_fee_per_day` properties reading `self.value[0]` and `self.value[1]`.

### REFACTOR Phase (`REFACTOR: model category rules as a CategoryPolicy and drop the unused rate constant`)

**Improvements Made**: `value[0]` and `value[1]` were unreadable, so the enum values became a
`NamedTuple`:

```python
class CategoryPolicy(NamedTuple):
    borrow_limit: int
    late_fee_per_day: float

class MemberCategory(Enum):
    STUDENT = CategoryPolicy(3, 1.00)
    FACULTY = CategoryPolicy(5, 0.50)
    PUBLIC = CategoryPolicy(2, 1.50)
```

The now-unused `LATE_FEE_PER_DAY` constant was deleted.

**Design Decision**: I did not design this up front. One integer, then a tuple, then a named
structure, each step forced by the next test. The 7 tests covering categories never changed during
the refactor.

---

## Other cycles in the history

Reservations (queue position, rejecting available books, FIFO order, duplicates, unknown members,
notifying the first reserver through an injected `notifier` mock, clearing the queue entry on
borrow) and the remaining `Book`/`Member`/`Library` behavior followed the same loop; see the
`RED:`/`GREEN:` pairs in the log.
