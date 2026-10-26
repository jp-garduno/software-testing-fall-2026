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


def test_total_overdue_fees(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 2))
    assert library.calculate_late_fees("m1", as_of=date(2026, 10, 18)) == 5


def test_record_return_date(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 17))
    assert library.loans[0]["returned_on"] == date(2026, 10, 17)
