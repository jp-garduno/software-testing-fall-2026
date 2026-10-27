from datetime import date

import pytest

from book import Book
from library import Library
from member import Member, MemberCategory


@pytest.fixture(name="library")
def fixture_library(clock):
    library = Library(clock=clock)
    library.add_book(Book("0306406152", "Clean Code", "Robert Martin", total_copies=2))
    library.register_member(Member("M001", "Ada Lovelace"))
    library.register_member(Member("M002", "Grace Hopper"))
    return library


def test_loan_is_due_fourteen_days_after_borrowing(library):
    loan = library.borrow_book("M001", "0306406152")

    assert loan.due_on == date(2026, 10, 15)


def test_no_late_fee_when_returned_on_the_due_date(library, clock):
    library.borrow_book("M001", "0306406152")
    clock.advance(14)
    library.return_book("M001", "0306406152")

    assert library.calculate_late_fees("M001") == 0


def test_overdue_loan_costs_one_dollar_per_day(library, clock):
    library.borrow_book("M001", "0306406152")
    clock.advance(17)

    assert library.calculate_late_fees("M001") == 300


def test_late_fee_stops_growing_once_the_book_is_returned(library, clock):
    library.borrow_book("M001", "0306406152")
    clock.advance(16)
    library.return_book("M001", "0306406152")
    clock.advance(10)

    assert library.calculate_late_fees("M001") == 200


def test_late_fees_only_count_the_members_own_loans(library, clock):
    library.borrow_book("M001", "0306406152")
    library.borrow_book("M002", "0306406152")
    clock.advance(15)

    assert library.calculate_late_fees("M002") == 100


def test_faculty_pays_half_the_daily_late_fee(library, clock):
    library.register_member(Member("F001", "Donald Knuth", MemberCategory.FACULTY))
    library.borrow_book("F001", "0306406152")
    clock.advance(18)

    assert library.calculate_late_fees("F001") == 200
