from unittest.mock import Mock

import pytest

from book import Book
from exceptions import MemberNotFoundError, ReservationError
from library import Library
from member import Member

ISBN = "0306406152"


@pytest.fixture
def notifier():
    return Mock()


def build_busy_library(clock, notifier=None):
    """Library whose only copy is lent to M001 while M002 and M003 wait."""
    library = Library(clock=clock, notifier=notifier)
    library.add_book(Book(ISBN, "Clean Code", "Robert C. Martin"))
    for member_id in ("M001", "M002", "M003"):
        library.register_member(Member(member_id, f"Member {member_id}"))
    library.borrow_book("M001", ISBN)
    return library


@pytest.fixture
def busy_library(clock, notifier):
    return build_busy_library(clock, notifier)


def test_reservations_are_kept_in_fifo_order(busy_library):
    busy_library.reserve_book("M002", ISBN)
    busy_library.reserve_book("M003", ISBN)
    assert busy_library.reservations_for(ISBN) == ["M002", "M003"]


def test_reserve_book_rejects_book_with_copies(library):
    with pytest.raises(ReservationError):
        library.reserve_book("M001", ISBN)


def test_reserve_book_rejects_unknown_member(busy_library):
    with pytest.raises(MemberNotFoundError):
        busy_library.reserve_book("M999", ISBN)


def test_return_book_notifies_first_member_in_queue(busy_library, notifier):
    busy_library.reserve_book("M002", ISBN)
    busy_library.reserve_book("M003", ISBN)
    busy_library.return_book("M001", ISBN)
    notifier.notify.assert_called_once_with("M002", busy_library.get_book(ISBN))


def test_reservations_advance_without_notifier(clock):
    library = build_busy_library(clock)
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)
    assert library.reservations_for(ISBN) == []
