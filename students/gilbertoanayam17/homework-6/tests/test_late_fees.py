"""Tests for late fees in Library: a mocked clock moves time forward without waiting."""

from datetime import date
from unittest.mock import Mock

from src.book import Book
from src.library import Library
from src.member import Member

ISBN = "1234567890"
BORROWED_ON = date(2026, 1, 1)


def make_library(clock):
    """Arrange a library on the given clock with one book and one member, M1."""
    library = Library(clock=clock)
    library.add_book(Book(ISBN, "Clean Code", "Robert C. Martin"))
    library.register_member(Member("M1", "Ana Lopez"))
    return library


def test_should_owe_nothing_while_no_loan_is_overdue():
    clock = Mock(return_value=BORROWED_ON)
    library = make_library(clock)
    library.borrow_book("M1", ISBN)

    assert library.calculate_late_fees("M1") == 0


def test_should_charge_one_dollar_per_day_for_overdue_loan():
    clock = Mock(return_value=BORROWED_ON)
    library = make_library(clock)
    library.borrow_book("M1", ISBN)

    clock.return_value = date(2026, 1, 20)

    assert library.calculate_late_fees("M1") == 5.0
