from unittest.mock import Mock

import pytest

from book import Book
from library import Library
from member import Member

ISBN = "1234567890"
OTHER_ISBN = "0987654321"


@pytest.fixture
def notifier():
    return Mock()


@pytest.fixture
def library(notifier):
    lib = Library(notifier=notifier)
    lib.add_book(Book(ISBN, "Popular Book", "Author", copies=1))
    for member_id in ("m1", "m2", "m3"):
        lib.register_member(Member(member_id, member_id.upper()))
    lib.borrow_book("m1", ISBN)
    return lib


def test_reserving_an_unavailable_book_returns_queue_position(library):
    assert library.reserve_book("m2", ISBN) == 1


def test_cannot_reserve_an_available_book(library):
    library.add_book(Book(OTHER_ISBN, "Spare Book", "Author", copies=2))
    with pytest.raises(ValueError, match="available"):
        library.reserve_book("m2", OTHER_ISBN)


def test_reservation_queue_keeps_first_come_first_served_order(library):
    library.reserve_book("m2", ISBN)
    library.reserve_book("m3", ISBN)
    assert library.get_reservation_queue(ISBN) == ["m2", "m3"]


def test_member_cannot_reserve_the_same_book_twice(library):
    library.reserve_book("m2", ISBN)
    with pytest.raises(ValueError, match="already reserved"):
        library.reserve_book("m2", ISBN)


def test_unknown_member_cannot_reserve(library):
    with pytest.raises(ValueError, match="Member not found"):
        library.reserve_book("ghost", ISBN)


def test_first_member_in_queue_is_notified_on_return(library, notifier):
    library.reserve_book("m2", ISBN)
    library.reserve_book("m3", ISBN)
    library.return_book("m1", ISBN)
    notifier.assert_called_once_with("m2", ISBN)


def test_borrowing_clears_the_members_reservation(library):
    library.reserve_book("m2", ISBN)
    library.return_book("m1", ISBN)
    library.borrow_book("m2", ISBN)
    assert library.get_reservation_queue(ISBN) == []
