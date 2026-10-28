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
