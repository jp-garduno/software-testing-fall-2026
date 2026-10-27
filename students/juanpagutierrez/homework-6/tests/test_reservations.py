"""Tests for the book reservation system (advanced feature 2)."""

from unittest.mock import Mock

import pytest

from src.book import Book
from src.library import Library
from src.member import Member

ISBN = "1234567890"


@pytest.fixture(name="notifier")
def notifier_fixture():
    """Stands in for an email/SMS service so tests stay fast and offline."""
    return Mock()


@pytest.fixture(name="library")
def library_fixture(notifier):
    """A single-copy book already lent to M001, plus members M002 and M003."""
    library = Library(notifier=notifier)
    library.add_book(Book(ISBN, "Clean Code", "Robert Martin"))
    for member_id, name in [("M001", "Ada Lovelace"), ("M002", "Grace Hopper"), ("M003", "Alan Turing")]:
        library.register_member(Member(member_id, name))
    library.borrow_book("M001", ISBN)
    return library


def test_member_can_reserve_an_unavailable_book(library):
    library.reserve_book("M002", ISBN)
    assert library.get_reservation_queue(ISBN) == ["M002"]
