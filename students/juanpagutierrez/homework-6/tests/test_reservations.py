"""Tests for the book reservation system (advanced feature 2)."""

from unittest.mock import Mock

import pytest

from src.book import Book
from src.exceptions import BookUnavailableError, ReservationError
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


def test_reservations_are_kept_in_first_come_first_served_order(library):
    library.reserve_book("M003", ISBN)
    library.reserve_book("M002", ISBN)
    assert library.get_reservation_queue(ISBN) == ["M003", "M002"]


def test_reserving_a_book_with_copies_on_the_shelf_raises(library):
    library.add_book(Book("0987654321", "Refactoring", "Martin Fowler"))
    with pytest.raises(ReservationError):
        library.reserve_book("M002", "0987654321")


def test_member_cannot_reserve_the_same_book_twice(library):
    library.reserve_book("M002", ISBN)
    with pytest.raises(ReservationError):
        library.reserve_book("M002", ISBN)


def test_returning_a_reserved_book_notifies_the_first_member_in_line(library, notifier):
    library.reserve_book("M002", ISBN)
    library.reserve_book("M003", ISBN)
    library.return_book("M001", ISBN)
    notifier.notify.assert_called_once_with("M002", ISBN)


def test_returned_copy_is_held_for_the_notified_member(library):
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)
    with pytest.raises(BookUnavailableError):
        library.borrow_book("M003", ISBN)
