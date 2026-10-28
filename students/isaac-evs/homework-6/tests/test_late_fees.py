from datetime import date

import pytest

from book import Book
from library import Library
from member import Member

ISBN = "1234567890"
OTHER_ISBN = "0987654321"


@pytest.fixture
def library(clock):
    lib = Library(clock=clock)
    lib.register_member(Member("m1", "Alice"))
    lib.add_book(Book(ISBN, "Book One", "Author", copies=2))
    lib.add_book(Book(OTHER_ISBN, "Book Two", "Author", copies=2))
    return lib


def test_due_date_is_14_days_after_borrowing(library):
    library.borrow_book("m1", ISBN)
    assert library.get_due_date("m1", ISBN) == date(2026, 1, 15)


def test_no_late_fee_on_the_due_date(library, clock):
    library.borrow_book("m1", ISBN)
    clock.advance(14)
    assert library.calculate_late_fee("m1", ISBN) == 0


def test_late_fee_is_one_dollar_per_overdue_day(library, clock):
    library.borrow_book("m1", ISBN)
    clock.advance(17)
    assert library.calculate_late_fee("m1", ISBN) == 3


def test_member_total_fees_add_up_across_loans(library, clock):
    library.borrow_book("m1", ISBN)
    clock.advance(2)
    library.borrow_book("m1", OTHER_ISBN)
    clock.advance(17)
    assert library.calculate_member_late_fees("m1") == 8


def test_returned_books_no_longer_accrue_fees(library, clock):
    library.borrow_book("m1", ISBN)
    clock.advance(19)
    library.return_book("m1", ISBN)
    assert library.calculate_member_late_fees("m1") == 0
