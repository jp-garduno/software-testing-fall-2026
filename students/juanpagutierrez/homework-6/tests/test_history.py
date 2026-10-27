"""Tests for borrowing history and statistics (advanced feature 4)."""

from datetime import date, timedelta
from unittest.mock import Mock

import pytest

from src.book import Book
from src.library import Library
from src.member import Member

CLEAN_CODE = "1234567890"
REFACTORING = "0987654321"


@pytest.fixture(name="clock")
def clock_fixture():
    """A controllable clock standing in for date.today."""
    return Mock(return_value=date(2026, 3, 1))


@pytest.fixture(name="library")
def library_fixture(clock):
    """A library with two books and two members."""
    library = Library(clock=clock)
    library.add_book(Book(CLEAN_CODE, "Clean Code", "Robert Martin", total_copies=2))
    library.add_book(Book(REFACTORING, "Refactoring", "Martin Fowler", total_copies=2))
    library.register_member(Member("M001", "Ada Lovelace"))
    library.register_member(Member("M002", "Grace Hopper"))
    return library


def test_history_report_lists_each_loan_with_its_status(library, clock):
    library.borrow_book("M001", CLEAN_CODE)
    clock.return_value += timedelta(days=3)
    library.return_book("M001", CLEAN_CODE)
    library.borrow_book("M001", REFACTORING)
    assert library.generate_history_report("M001") == [
        "History for Ada Lovelace (M001)",
        "2026-03-01 Clean Code - returned 2026-03-04",
        "2026-03-04 Refactoring - on loan, due 2026-03-18",
        "Total loans: 2",
    ]


def test_most_borrowed_book_counts_loans_across_all_members(library):
    library.borrow_book("M001", REFACTORING)
    library.borrow_book("M002", REFACTORING)
    library.borrow_book("M002", CLEAN_CODE)
    assert library.most_borrowed_book().isbn == REFACTORING


def test_most_borrowed_book_is_none_when_nothing_was_lent(library):
    assert library.most_borrowed_book() is None
