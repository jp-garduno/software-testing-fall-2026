from datetime import date
import pytest
from src.book import Book
from src.library import Library
from src.member import Member


def test_loan_due_date(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    loan = library.loans[0]
    assert (loan["member_id"], loan["isbn"], loan["borrowed_on"], loan["due_on"]) == (
        "m1", "1234567890", date(2026, 10, 1), date(2026, 10, 15))
