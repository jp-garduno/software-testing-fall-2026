from datetime import date
from decimal import Decimal

import pytest

from src.book import Book
from src.library import Library
from src.loan import Loan
from src.member import Member


def test_loan_records_member_book_and_borrow_date():
    loan = Loan("M1", "1234567890", date(2026, 1, 1))
    assert (loan.member_id, loan.isbn, loan.borrowed_on) == ("M1", "1234567890", date(2026, 1, 1))


def test_due_date_crosses_month_boundary():
    loan = Loan("M1", "1234567890", date(2026, 1, 25))
    assert loan.due_date == date(2026, 2, 8)


@pytest.mark.parametrize("as_of, expected", [(date(2026, 1, 1), "0"), (date(2026, 1, 15), "0"), (date(2026, 1, 16), "1"), (date(2026, 1, 20), "5")])
def test_late_fee_respects_due_date_boundary(as_of, expected):
    assert Loan("M1", "1234567890", date(2026, 1, 1)).late_fee(as_of) == Decimal(expected)


def test_closed_loan_stops_fees_at_return_date():
    loan = Loan("M1", "1234567890", date(2026, 1, 1), returned_on=date(2026, 1, 18))
    assert loan.late_fee(date(2026, 2, 1)) == Decimal("3")


@pytest.mark.parametrize("category, expected", [("student", 3), ("faculty", 5), ("public", 2)])
def test_member_category_sets_borrowing_limit(category, expected):
    assert Member("M1", "Ana", category=category).max_borrow_limit == expected


@pytest.mark.parametrize("category", ["visitor", "Faculty", None, []])
def test_member_rejects_unknown_category(category):
    with pytest.raises(ValueError, match="category"):
        Member("M1", "Ana", category=category)


@pytest.mark.parametrize("category, expected", [("student", "1"), ("faculty", "0.50"), ("public", "1.50")])
def test_member_category_sets_daily_fee_rate(category, expected):
    assert Member("M1", "Ana", category=category).daily_fee_rate == Decimal(expected)


def test_loan_captures_category_rate():
    loan = Loan("M1", "1234567890", date(2026, 1, 1), daily_rate=Decimal("0.50"))
    assert loan.late_fee(date(2026, 1, 18)) == Decimal("1.50")


def test_library_uses_injected_borrow_date():
    library = Library(today=lambda: date(2026, 1, 1))
    library.add_book(Book("1234567890", "Title", "Author"))
    library.register_member(Member("M1", "Ana"))
    assert library.borrow_book("M1", "1234567890").due_date == date(2026, 1, 15)


@pytest.fixture
def dated_library():
    clock = [date(2026, 1, 1)]
    library = Library(today=lambda: clock[0])
    library.add_book(Book("1234567890", "Title", "Author", 2))
    library.register_member(Member("M1", "Ana"))
    return library, clock


def test_new_member_has_empty_history(dated_library):
    library, _ = dated_library
    assert library.get_member_history("M1") == ()
