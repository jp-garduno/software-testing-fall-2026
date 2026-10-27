# TDD Process: Five Red-Green-Refactor Cycles

This document walks through five of the 68 cycles in this project. They show the design changing over time: a "fake it"
first step, a bug that a test caught before it shipped, time injected so it could be controlled, a class pulled out of a
growing facade, and a refactor pushed by the linter. The test failures quoted are the real output, copied from the
runs logged during development.

The full history is in `git log`. Each `RED:` commit was made only after the suite was seen to fail, and each `GREEN:`
or `REFACTOR:` commit only after it passed.

---

## Cycle #1: Book Availability (fake it, then triangulate)

### RED Phase

**Test Written** (commit `RED: should report book as available when copies exist`):

```python
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=1)
    assert book.is_available() is True
```

**Test Result**: FAIL

```
E       AttributeError: 'Book' object has no attribute 'is_available'
FAILED tests/test_book.py::test_book_is_available_when_copies_exist
1 failed, 2 passed in 0.14s
```

### GREEN Phase

**Code Written** (commit `GREEN: add is_available returning True`). This is the smallest code that passes:

```python
    def is_available(self):
        """Return True while at least one copy is on the shelf."""
        return True
```

**Test Result**: PASS (3 passed)

Returning a constant looks silly, but one test cannot tell "always true" apart from "true when copies exist". So I
wrote a second test that can (*triangulation*):

```python
def test_book_is_not_available_when_no_copies():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=0)
    assert book.is_available() is False
```

```
FAILED tests/test_book.py::test_book_is_not_available_when_no_copies - assert True is False
1 failed, 3 passed in 0.14s
```

Then the real implementation (commit `GREEN: base is_available on available_copies`):

```python
    def is_available(self):
        return self.available_copies > 0
```

### REFACTOR Phase

**Improvements Made**: None at this step. A few cycles later, after ISBN, title and copy-count validation had piled up
in `__init__`, I pulled each rule into its own helper (`REFACTOR: extract Book validation rules into named helpers`).
When `Member` needed the same "required text" check, it moved to `src/validation.py`
(`REFACTOR: share blank-text validation between Book and Member`).

**Design Decision**: `is_available()` returns a boolean, not a count. Callers (`borrow()`, `get_available_books()`,
reservations) only ever ask "can I take one?". The count is still available as `available_copies` for anyone who needs
it.

---

## Cycle #2: A Failed Borrow Must Not Lose a Copy (a test that found a bug)

### RED Phase

Up to this point, `Library.borrow_book` was the simplest version that passed its tests:

```python
    def borrow_book(self, member_id, isbn):
        self.get_book(isbn).borrow()
        self.get_member(member_id).add_borrowed_book(isbn)
```

`Member.add_borrowed_book` already raises `BorrowLimitExceededError`, so the limit *looked* enforced. To check what
happens to the book when that error fires, I wrote this test:

```python
def test_failed_borrow_over_limit_keeps_the_copy_on_the_shelf(library):
    library.add_book(Book("0987654321", "Refactoring", "Martin Fowler", total_copies=2))
    library.register_member(Member("M002", "Grace Hopper", max_borrow_limit=0))
    with pytest.raises(BorrowLimitExceededError):
        library.borrow_book("M002", "0987654321")
    assert library.get_book("0987654321").available_copies == 2
```

**Test Result**: FAIL. The error was raised, but only *after* a copy had been taken off the shelf:

```
E       AssertionError: assert 1 == 2
E        +  where 1 = <src.book.Book object at 0x...>.available_copies
FAILED tests/test_library.py::test_failed_borrow_over_limit_keeps_the_copy_on_the_shelf
1 failed, 37 passed in 0.21s
```

### GREEN Phase

**Code Written** (commit `GREEN: check the member limit before taking a copy off the shelf`):

```python
    def borrow_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        if not member.can_borrow():
            raise BorrowLimitExceededError(f"{member_id} reached the limit of {member.max_borrow_limit}")
        book.borrow()
        member.add_borrowed_book(isbn)
```

**Test Result**: PASS (38 passed)

### REFACTOR Phase

**Improvements Made**: None needed. The method now reads as "look everything up, check every rule, then change state".

**Design Decision**: All checks happen before any state changes, so a failed operation leaves no trace. Every later
feature followed this rule. The reservation hold check (Cycle #4) is placed before `book.borrow()` for the same reason.
Next I added the opposite case, borrowing a book with no copies left
(`TEST: confirm borrowing an unavailable book leaves the member unchanged`). It passed on the first run, because
`book.borrow()` already raises before the member is touched. I committed it as `TEST:` rather than `RED:`, because a test
that never failed is not a RED step.

---

## Cycle #3: Late Fees Stop Growing on Return (injected clock + mocks)

### RED Phase

The first fee test only covered books still on loan. The GREEN step for it counted every loan up to *today*, which was
enough for that test. The next test asked what happens after the book comes back:

```python
def test_fee_stops_growing_once_the_book_is_returned(library, clock):
    library.borrow_book(MEMBER_ID, ISBN)
    advance(clock, 14 + 2)
    library.return_book(MEMBER_ID, ISBN)
    advance(clock, 10)
    assert library.calculate_member_fees(MEMBER_ID) == Decimal("2.00")
```

`clock` is a `Mock(return_value=date(2026, 3, 1))` passed to `Library(clock=clock)`, and `advance` moves its
`return_value` forward. The test covers 26 days and runs in about a millisecond.

**Test Result**: FAIL. The fee kept growing after the return:

```
E       AssertionError: assert Decimal('12.00') == Decimal('2.00')
FAILED tests/test_library_fees.py::test_fee_stops_growing_once_the_book_is_returned
1 failed, 59 passed in 0.28s
```

### GREEN Phase

**Code Written** (commit `GREEN: use the return date for fees of returned loans`), a one-line change:

```python
        return sum((calculate_late_fee(loan.due_date, loan.returned_on or today) for loan in self.get_loans(member_id)),
                   Decimal("0"))
```

**Test Result**: PASS (60 passed). The next cycle added the category rate (`RED: should charge each member at their
category rate`, which failed with `Decimal('4.00') == Decimal('2.00')` for a faculty member).

### REFACTOR Phase

**Improvements Made** (commit `REFACTOR: move per-loan fee calculation into Loan`). `Library` was reaching into loans
to work out dates. That knowledge now lives on the `Loan` itself:

```python
@dataclass
class Loan:
    ...
    @property
    def is_open(self):
        return self.returned_on is None

    def late_fee(self, today, daily_rate):
        end = today if self.is_open else self.returned_on
        return calculate_late_fee(self.due_date, end, daily_rate)
```

```python
    def calculate_member_fees(self, member_id):
        today = self._clock()
        rate = self.get_member(member_id).daily_late_fee
        return sum((loan.late_fee(today, rate) for loan in self.get_loans(member_id)), Decimal("0"))
```

**Design Decision**: The tests needed control over time, which led to injecting the clock
(`Library(clock=date.today)` in production). Without TDD I would probably have called `date.today()` inside
`borrow_book` and then had to patch it. I also chose `Decimal` over `float` the first time a fee appeared in a test
(`Decimal("0.50")`): with floats, an assertion like `== 2.00` can fail because of rounding.

---

## Cycle #4: Holding a Returned Copy for the Next in Line (and extracting a class)

### RED Phase

At first, returning a reserved book notified the first member in line (checked with a `Mock` notifier and
`assert_called_once_with`). But nothing stopped someone else from taking the copy right after the notification. The test:

```python
def test_returned_copy_is_held_for_the_notified_member(library):
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)
    with pytest.raises(BookUnavailableError):
        library.borrow_book("M003", ISBN)
```

**Test Result**: FAIL

```
E       Failed: DID NOT RAISE BookUnavailableError
FAILED tests/test_reservations.py::test_returned_copy_is_held_for_the_notified_member
1 failed, 70 passed in 0.27s
```

### GREEN Phase

**Code Written** (commit `GREEN: hold returned copies for members notified of their reservation`). Notified members go
into a `_holds` list, and `borrow_book` refuses anyone else while every free copy is held:

```python
        holds = self._holds.get(isbn, [])
        if member_id not in holds and book.available_copies <= len(holds):
            raise BookUnavailableError(f"The free copies of {isbn} are held for members who reserved it")
```

**Test Result**: PASS (71 passed)

This GREEN step had a gap: the hold was never released. The next RED test showed it: after M002 borrowed and returned
the book, M003 still could not borrow it (`BookUnavailableError: The free copies of 1234567890 are held...`). A further
RED test showed that a `Library()` with no notifier crashed on `None.notify`. Both got small GREEN fixes.

### REFACTOR Phase

**Improvements Made** (commit `REFACTOR: extract ReservationDesk from Library`). Reservation logic was now spread over
four `Library` methods and two dictionaries. I moved it into its own class and kept the tests unchanged:

```python
class ReservationDesk:
    def reserve(self, member_id, isbn): ...          # FIFO queue (deque), rejects duplicates
    def queue(self, isbn): ...
    def copy_returned(self, isbn): ...               # pop next, hold the copy, notify
    def blocks(self, member_id, isbn, available_copies): ...
    def release(self, member_id, isbn): ...
```

`Library` now only makes calls such as `self._reservations.blocks(...)` and `self._reservations.copy_returned(isbn)`.

**Design Decision**: All 74 tests stayed the same through this change, because they test the behavior of `Library`,
not its internal dictionaries. That is why the extraction was safe. If the tests had checked `library._holds`, the
refactor would have broken them even though nothing was wrong. I also switched the queue from a list with `pop(0)` to a
`deque`, which suits a first-in, first-out queue better.

---

## Cycle #5: Sorting When Some Books Have No Rating (and a refactor driven by the linter)

### RED Phase

Search could already filter and sort. I then asked what happens when a book has no rating and you sort by rating:

```python
def test_books_missing_the_sort_field_are_listed_last(library):
    library.add_book(Book("5555555555", "Untitled Draft", "Anonymous", details=BookDetails(genre="Software")))
    assert isbns(library.search(genre="Software", sort_by="rating", descending=True)) == [
        "1111111111", "3333333333", "5555555555"]
```

**Test Result**: FAIL with a crash, not just a wrong answer:

```
E           TypeError: '<' not supported between instances of 'float' and 'NoneType'
FAILED tests/test_search.py::test_books_missing_the_sort_field_are_listed_last
1 failed, 84 passed in 0.30s
```

### GREEN Phase

**Code Written** (commit `GREEN: place books without a value for the sort field last`):

```python
def _sorted(books, field, descending):
    """Sort by ``field``; books without a value always go last."""
    with_value = [book for book in books if getattr(book, field) is not None]
    without_value = [book for book in books if getattr(book, field) is None]
    with_value.sort(key=lambda book: getattr(book, field), reverse=descending)
    return with_value + without_value
```

**Test Result**: PASS (85 passed)

### REFACTOR Phase

**Improvements Made**: Pylint (the version the grader uses) flagged `search_books(books, genre, publication_year,
min_rating, sort_by, descending)` for too many arguments. Since the tests call `library.search(**filters)`, I could
change the inside freely. The parameters became a frozen value object (`REFACTOR: replace search_books parameters with a
SearchQuery value object`):

```python
@dataclass(frozen=True)
class SearchQuery:
    genre: Optional[str] = None
    publication_year: Optional[int] = None
    min_rating: Optional[float] = None
    sort_by: Optional[str] = None
    descending: bool = False

    def matches(self, book): ...
    def run(self, books): ...
```

The same problem with `Book(..., genre, publication_year, rating)` led to a `BookDetails` value object. The 0-5 rating
check moved into `BookDetails.__post_init__`, next to the data it checks.

**Design Decision**: The linter warning pointed to a real design problem: a group of values that always travel together
but had no name. `SearchQuery` checks the sort field when it is created, so an invalid query cannot exist. It can also be
built and passed around before running it. The `SearchQuery` change needed no test edits, because it was internal.
`BookDetails` changed `Book`'s public constructor, so the search tests that build books with metadata were updated in
the same commit. The suite was green before and after every one of these commits.

---

## Summary of the evolution

| Stage | Tests | Shape of the design |
| --- | --- | --- |
| Book + Member | 29 | Two plain classes with validation |
| Library core | 45 | Facade over dictionaries of books and members |
| Categories + late fees | 61 | `MemberCategory` enum, `Loan` records, injected `clock` |
| History + reservations | 74 | `history` module, `ReservationDesk`, injected `notifier` |
| Search | 85 | `SearchQuery` and `BookDetails` value objects |

I didn't plan any of these classes up front. Each one appeared during a REFACTOR step, once the tests showed a group
of behavior that belonged together.
