"""Tests for the reservation queue."""
# pylint: disable=missing-function-docstring

import pytest

from src.errors import LibraryError
from src.member import Member
from tests.helpers import ISBN, make_library


def make_busy_library():
    """Library whose only copy is on loan to m1, with m2 and m3 registered."""
    library = make_library()
    library.register_member(Member("m2", "Bo"))
    library.register_member(Member("m3", "Cy"))
    library.borrow_book("m1", ISBN)
    return library


def test_reserving_a_borrowed_book_adds_member_to_queue():
    library = make_busy_library()
    library.reserve_book("m2", ISBN)
    assert library.reservation_queue(ISBN) == ["m2"]


def test_reserving_an_available_book_raises_error():
    library = make_library()
    with pytest.raises(LibraryError):
        library.reserve_book("m1", ISBN)


def test_queue_keeps_first_come_first_served_order():
    library = make_busy_library()
    library.reserve_book("m3", ISBN)
    library.reserve_book("m2", ISBN)
    assert library.reservation_queue(ISBN) == ["m3", "m2"]


def test_member_cannot_reserve_the_same_book_twice():
    library = make_busy_library()
    library.reserve_book("m2", ISBN)
    with pytest.raises(LibraryError):
        library.reserve_book("m2", ISBN)


def test_return_notifies_the_first_member_in_line():
    library = make_busy_library()
    library.reserve_book("m2", ISBN)
    library.reserve_book("m3", ISBN)
    library.return_book("m1", ISBN)
    assert library.notifications == [("m2", ISBN)]


def test_notified_member_leaves_the_queue():
    library = make_busy_library()
    library.reserve_book("m2", ISBN)
    library.reserve_book("m3", ISBN)
    library.return_book("m1", ISBN)
    assert library.reservation_queue(ISBN) == ["m3"]


def test_return_without_reservations_sends_no_notification():
    library = make_busy_library()
    library.return_book("m1", ISBN)
    assert library.notifications == []
