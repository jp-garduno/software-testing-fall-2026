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
