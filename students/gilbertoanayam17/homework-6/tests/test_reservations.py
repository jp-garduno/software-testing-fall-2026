"""Tests for reservations: a FIFO queue per book and a notification when a copy comes back."""

import pytest

from src import errors
from src.book import Book
from src.library import Library
from src.member import Member

ISBN = "1234567890"


def make_library():
    """Arrange a library whose only copy is lent to M1, with M2 and M3 also registered."""
    library = Library()
    library.add_book(Book(ISBN, "Clean Code", "Robert C. Martin", copies=1))
    for member_id in ("M1", "M2", "M3"):
        library.register_member(Member(member_id, f"Member {member_id}"))
    library.borrow_book("M1", ISBN)
    return library


def test_should_queue_member_who_reserves_unavailable_book():
    library = make_library()

    library.reserve_book("M2", ISBN)

    assert library.get_reservations(ISBN) == ["M2"]


def test_should_reject_reservation_while_copies_are_available():
    library = make_library()
    library.return_book("M1", ISBN)

    with pytest.raises(errors.BookAvailableError):
        library.reserve_book("M2", ISBN)
