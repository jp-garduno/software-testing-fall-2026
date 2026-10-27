"""Tests for late fees integrated with Library lending (advanced feature 1)."""

from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import Mock

import pytest

from src.book import Book
from src.library import Library
from src.member import Member, MemberCategory

ISBN = "1234567890"
MEMBER_ID = "M001"
START = date(2026, 3, 1)


@pytest.fixture(name="clock")
def clock_fixture():
    """A controllable clock standing in for date.today."""
    return Mock(return_value=START)


@pytest.fixture(name="library")
def library_fixture(clock):
    """A library on a fake clock, with one book and one student member."""
    library = Library(clock=clock)
    library.add_book(Book(ISBN, "Clean Code", "Robert Martin"))
    library.register_member(Member(MEMBER_ID, "Ada Lovelace"))
    return library


def advance(clock, days):
    """Move the fake clock forward by ``days``."""
    clock.return_value = clock.return_value + timedelta(days=days)


def test_borrowing_records_a_loan_due_in_fourteen_days(library):
    library.borrow_book(MEMBER_ID, ISBN)
    assert library.get_loans(MEMBER_ID)[0].due_date == date(2026, 3, 15)


def test_returning_closes_the_loan_with_todays_date(library, clock):
    library.borrow_book(MEMBER_ID, ISBN)
    advance(clock, 3)
    library.return_book(MEMBER_ID, ISBN)
    assert library.get_loans(MEMBER_ID)[0].returned_on == date(2026, 3, 4)


def test_member_owes_one_dollar_per_day_for_an_overdue_book(library, clock):
    library.borrow_book(MEMBER_ID, ISBN)
    advance(clock, 14 + 5)
    assert library.calculate_member_fees(MEMBER_ID) == Decimal("5.00")


def test_fee_stops_growing_once_the_book_is_returned(library, clock):
    library.borrow_book(MEMBER_ID, ISBN)
    advance(clock, 14 + 2)
    library.return_book(MEMBER_ID, ISBN)
    advance(clock, 10)
    assert library.calculate_member_fees(MEMBER_ID) == Decimal("2.00")


def test_faculty_member_is_charged_the_faculty_rate(library, clock):
    library.register_member(Member("F001", "Alan Turing", category=MemberCategory.FACULTY))
    library.borrow_book("F001", ISBN)
    advance(clock, 14 + 4)
    assert library.calculate_member_fees("F001") == Decimal("2.00")
