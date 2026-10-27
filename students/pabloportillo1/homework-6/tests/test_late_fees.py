from datetime import date

import pytest

from book import Book
from library import Library
from member import Member


@pytest.fixture(name="library")
def fixture_library(clock):
    library = Library(clock=clock)
    library.add_book(Book("0306406152", "Clean Code", "Robert Martin", total_copies=2))
    library.register_member(Member("M001", "Ada Lovelace"))
    return library


def test_loan_is_due_fourteen_days_after_borrowing(library):
    loan = library.borrow_book("M001", "0306406152")

    assert loan.due_on == date(2026, 10, 15)
