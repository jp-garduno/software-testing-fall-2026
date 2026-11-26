# TDD Process — Library Management System

Every test in this project was committed in a failing state before the code that makes it pass.
I did not take this on trust: each step went through a small script that ran the whole suite, refused to
commit a `RED` step if the suite passed, and refused to commit a `GREEN` or `REFACTOR` step if anything
failed. The test output quoted below is the real output saved at each `RED` step.

The TDD history has 290 commits: 135 RED, 135 GREEN, 18 REFACTOR, plus one scaffold and one
coverage commit. Commits follow Conventional Commits with the phase in the subject, because the repository's
commit-msg hook rejects anything else:

```
test(homework-6): RED should accept a thirteen digit isbn
feat(homework-6): GREEN accept isbn-10 and isbn-13 lengths
refactor(homework-6): REFACTOR name the valid isbn lengths
```

The five cycles below are from the Python implementation; the JavaScript one followed the same path.

---

## Cycle #1: Book Availability Check

### RED Phase

The previous cycle had added `is_available()` with the simplest possible body, `return True`, because the
only test asked for a book *with* copies. This test makes that shortcut wrong:

```python
def test_book_without_copies_is_not_available():
    book = Book("0306406152", "Clean Code", "Robert Martin", total_copies=0)

    assert book.is_available() is False
```

**Test Result**: FAIL

```
E       assert True is False
E        +  where True = is_available()
FAILED tests/test_book.py::test_book_without_copies_is_not_available
1 failed, 3 passed in 0.03s
```

### GREEN Phase

```python
    def is_available(self):
        return self.available_copies > 0
```

**Test Result**: PASS — 4 passed

### REFACTOR Phase

**Improvements Made**: the four book tests each built the same `Book("0306406152", "Clean Code", ...)` by
hand. I extracted a `make_book(total_copies=1)` helper and an `ISBN` constant, so each test now shows only
the value it is about (the number of copies).

**Design Decision**: `is_available()` returns a boolean, not the count. Callers ask "can I borrow it?", and
the count is still there as `available_copies` for anyone who needs it. Writing `return True` first felt
silly, but it is what made the second test meaningful: the zero-copies test failed for exactly the reason
I expected, which proved it could catch the bug.

**Commits**: `f30a306` RED · `4cb39a3` GREEN · `8ebb52a` REFACTOR

---

## Cycle #2: ISBN-10 and ISBN-13

### RED Phase

The first validation cycle only had a nine-digit ISBN to reject, so the code checked `len(isbn) != 10`.
The next test asks for the other legal length:

```python
def test_isbn_with_thirteen_digits_is_accepted():
    assert Book("9780306406157", "Clean Code", "Robert Martin").isbn == "9780306406157"
```

**Test Result**: FAIL — the ten-only check rejects a valid ISBN-13

```
E           ValueError: ISBN must be 10 or 13 digits
FAILED tests/test_book.py::test_isbn_with_thirteen_digits_is_accepted
1 failed, 9 passed in 0.03s
```

### GREEN Phase

```python
        if len(isbn) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 digits")
```

**Test Result**: PASS — 10 passed

### REFACTOR Phase

One more RED/GREEN pair followed (`"03064O6152"`, with a letter O, must be rejected → `or not isbn.isdigit()`).
Then the condition read `len(isbn) not in (10, 13) or not isbn.isdigit()`, with a bare tuple whose meaning
you had to know. I named it:

```python
ISBN_LENGTHS = (10, 13)
...
        if len(isbn) not in ISBN_LENGTHS or not isbn.isdigit():
```

Two cycles later, with title and copy validation added too, the constructor had grown three guard clauses
before any assignment, so a second refactor moved them into a `_validate()` static method.

**Design Decision**: I triangulated, using three tests (9 digits, 13 digits, a letter) to force the general
rule instead of writing it up front. In the JavaScript version I wrote a regular expression
`/^(\d{10}|\d{13})$/` in the second GREEN step, which already rejected letters, so the letter test passed
the moment it was written. Being "too clever" in GREEN cost me a RED step; see the last section.

**Commits**: `3dddd4d` RED · `2e6bc5a` GREEN · `8d90838` REFACTOR

---

## Cycle #3: Borrowing Must Not Leave Half a Loan

### RED Phase

`borrow_book` changes two objects: the book loses a copy, the member gains an ISBN. The previous cycle had
reordered those two calls so that an unavailable book no longer left the member holding it. This test
checks the opposite failure, a member who is already at the limit:

```python
def test_borrowing_beyond_the_member_limit_leaves_the_copies_unchanged(library, book):
    for isbn in ("0131103628", "0201633612", "0596007124"):
        library.add_book(Book(isbn, f"Book {isbn}", "Author"))
        library.borrow_book("M001", isbn)

    with pytest.raises(ValueError, match="borrow limit"):
        library.borrow_book("M001", "0306406152")
    assert book.available_copies == 2
```

**Test Result**: FAIL — the book had already lost its copy when the member refused it

```
E       assert 1 == 2
E        +  where 1 = <book.Book object at 0x107181a10>.available_copies
FAILED tests/test_library.py::test_borrowing_beyond_the_member_limit_leaves_the_copies_unchanged
1 failed, 31 passed in 0.06s
```

### GREEN Phase

No order of the two calls satisfies both tests, so both checks have to happen before either change:

```python
    def borrow_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        if not book.is_available():
            raise ValueError(f"No copies available for '{book.title}'")
        member.add_borrowed_book(isbn)
        book.borrow()
```

**Test Result**: PASS — 32 passed

### REFACTOR Phase

**Improvements Made**: the error message `"No copies available for ..."` now lived in both `Book.borrow()` and
`Library.borrow_book()`. I moved the check into `Book.ensure_available()`, which `borrow()` and the library
both call, so the rule and its message exist once.

**Design Decision**: this was the most useful pair of tests in the project. Each test alone passes with one
of the two orderings, and only the pair forces "validate everything, then mutate". I would not have
written that second test without TDD, because the first ordering *looked* correct.

**Commits**: `e630890` RED · `a25feda` GREEN · `2988094` REFACTOR

---

## Cycle #4: The Late Fee Stops at the Return Date

### RED Phase

Late fees started as "days between today and the due date". That is right while the book is out, and wrong
once it comes back:

```python
def test_late_fee_stops_growing_once_the_book_is_returned(library, clock):
    library.borrow_book("M001", "0306406152")
    clock.advance(16)
    library.return_book("M001", "0306406152")
    clock.advance(10)

    assert library.calculate_late_fees("M001") == 200
```

**Test Result**: FAIL — the fee kept counting the 10 days after the return

```
E       AssertionError: assert 1200 == 200
E        +  where 1200 = calculate_late_fees('M001')
FAILED tests/test_late_fees.py::test_late_fee_stops_growing_once_the_book_is_returned
1 failed, 39 passed in 0.07s
```

### GREEN Phase

The loan records when it was returned, and the fee counts up to that date instead of today:

```python
# loan.py
        self.returned_on = None

# library.py, return_book
        loan = next(loan for loan in self._loans
                    if loan.member_id == member_id and loan.isbn == isbn and loan.returned_on is None)
        loan.returned_on = self._clock()

# library.py, calculate_late_fees
        return sum(max(0, ((loan.returned_on or today) - loan.due_on).days) * 100 for loan in self._loans)
```

**Test Result**: PASS — 40 passed

### REFACTOR Phase

**Improvements Made**: after the next cycle (only count the member's own loans) I did two refactors.
`Loan.days_overdue(today)` now owns the date arithmetic, so the library only multiplies by a rate. The
generator in `return_book` became `_active_loan(member_id, isbn)`, a name that says what it finds.

**Design Decision**: the library takes a `clock` function in its constructor (`date.today` by default).
Tests pass a `FakeClock` they can `advance(days)`. That made this test possible at all, since it needs
26 days to pass in a test that runs in milliseconds. The need for it showed up the moment I wrote the first
due-date test, which is the "design pressure" TDD is supposed to create.

**Commits**: `9288189` RED · `ffedb12` GREEN · `f69e66d`, `02f30bd` REFACTOR

---

## Cycle #5: A Held Copy Is Released Once Borrowed

### RED Phase

When a reserved book comes back, the copy is held for the first member in the queue. The hold must end
when that member borrows it, or the copy stays blocked for everyone forever:

```python
def test_hold_is_released_once_the_reserver_borrows_the_copy(library):
    library.borrow_book("M001", ISBN)
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)
    library.borrow_book("M002", ISBN)
    library.return_book("M002", ISBN)

    library.borrow_book("M003", ISBN)

    assert library.get_member("M003").borrowed_books == [ISBN]
```

**Test Result**: FAIL — M002 still had a hold on a copy they had already borrowed and returned

```
E           ValueError: The copy of 'Clean Code' is held for another member
FAILED tests/test_reservations.py::test_hold_is_released_once_the_reserver_borrows_the_copy
1 failed, 53 passed in 0.09s
```

### GREEN Phase

```python
        member.add_borrowed_book(isbn)
        book.borrow()
        if member_id in held:
            held.remove(member_id)
```

**Test Result**: PASS — 54 passed

### REFACTOR Phase

**Improvements Made**: two more cycles followed (a book whose only copy is held can still be reserved; a
missing notifier must not crash a return), and both needed "copies on the shelf minus copies on hold".
I named that `_free_copies(book)` and used it in both `borrow_book` and `reserve_book`. Then the
queue-to-hold-to-notify block in `return_book` became `_hold_for_next_reserver(book)`.

**Design Decision**: the notifier is injected and optional. Tests use `Mock(spec_set=["notify_available"])`,
which fails if the code calls any other method. The "no notifier" test exists because the first GREEN
called `self._notifier.notify_available` unconditionally, and a library without notifications would have
crashed on the first reserved return.

**Commits**: `71ee8c1` RED · `f8dce50` GREEN · `04609f5`, `9e965fc` REFACTOR

---

## When the Cycle Did Not Go to Plan

The script that enforced the cycle caught four steps where I got it wrong. I kept them in the history rather
than rewriting it:

1. **A RED test that passed (Python, sort by year).** My first test used the two fiction books, whose
   order by year happens to equal their order by title, which was already the default. The script refused to
   commit it. I replaced it with the software books, where the two orders differ, and only then wrote
   the code. A test that passes before the code exists proves nothing.
2. **GREEN went further than the test (JavaScript, ISBN).** The regular expression from the 13-digit step
   already rejected letters, so the letter test was green on arrival. It went in with the next RED commit.
3. **GREEN went further than the test (JavaScript, FIFO).** I used `queue.shift()` in the notify step, which
   already removes the member, so the first-come-first-served test was green on arrival too.
4. **A wrong expectation (JavaScript, sort by year).** I wrote that *The C Programming Language* (1988) comes
   second, but *To Kill a Mockingbird* (1960) is older. The implementation was right and my test was wrong.
   The fix went into the GREEN commit, and its message says so.

At the end, coverage showed one JavaScript fallback (`holds.get(isbn) ?? []`) that could never run, because
`borrowBook` rewrote the holds entry on every borrow. A refactor made JavaScript only touch holds when
the borrower held a copy, as the Python code already did. Two tests that pass without new code, both
committed as `test:` rather than `RED`, cover holding two copies at once and an empty queue.
