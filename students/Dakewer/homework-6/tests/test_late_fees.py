from datetime import date, timedelta

import pytest

from src.book import Book
from src.library import Library
from src.member import Member

BORROW_DATE = date(2026, 1, 1)


@pytest.fixture
def library():
    lib = Library()
    lib.add_book(Book("1234567890", "Clean Code", "Robert Martin", copies=2))
    lib.add_book(Book("0987654321", "Refactoring", "Martin Fowler", copies=2))
    lib.register_member(Member("M001", "Alice"))
    return lib


def test_due_date_is_14_days_after_borrow(library):
    library.borrow_book("M001", "1234567890", borrow_date=BORROW_DATE)
    assert library.get_due_date("M001", "1234567890") == date(2026, 1, 15)


def test_borrow_date_defaults_to_today(library):
    library.borrow_book("M001", "1234567890")
    assert library.get_due_date("M001", "1234567890") == date.today() + timedelta(days=14)


def test_no_late_fee_before_due_date(library):
    library.borrow_book("M001", "1234567890", borrow_date=BORROW_DATE)
    assert library.calculate_late_fee("M001", as_of=date(2026, 1, 10)) == 0


def test_late_fee_is_one_dollar_per_overdue_day(library):
    library.borrow_book("M001", "1234567890", borrow_date=BORROW_DATE)
    assert library.calculate_late_fee("M001", as_of=date(2026, 1, 20)) == 5


def test_returned_books_no_longer_accrue_fees(library):
    library.borrow_book("M001", "1234567890", borrow_date=BORROW_DATE)
    library.return_book("M001", "1234567890")
    assert library.calculate_late_fee("M001", as_of=date(2026, 3, 1)) == 0


def test_return_book_reports_fee_for_that_loan(library):
    library.borrow_book("M001", "1234567890", borrow_date=BORROW_DATE)
    fee = library.return_book("M001", "1234567890", return_date=date(2026, 1, 20))
    assert fee == 5
