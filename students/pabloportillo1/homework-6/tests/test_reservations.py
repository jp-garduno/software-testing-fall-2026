from unittest.mock import Mock

import pytest

from book import Book
from library import Library
from member import Member

ISBN = "0306406152"


@pytest.fixture(name="notifier")
def fixture_notifier():
    return Mock(spec_set=["notify_available"])


@pytest.fixture(name="library")
def fixture_library(clock, notifier):
    library = Library(clock=clock, notifier=notifier)
    library.add_book(Book(ISBN, "Clean Code", "Robert Martin", total_copies=1))
    for member_id, name in (("M001", "Ada Lovelace"), ("M002", "Grace Hopper"), ("M003", "Alan Turing")):
        library.register_member(Member(member_id, name))
    return library


def test_reserving_a_book_with_no_copy_left_queues_the_member(library):
    library.borrow_book("M001", ISBN)

    library.reserve_book("M002", ISBN)

    assert library.reservations_for(ISBN) == ["M002"]


def test_reserving_a_book_on_the_shelf_is_rejected(library):
    with pytest.raises(ValueError, match="is available, borrow it instead"):
        library.reserve_book("M002", ISBN)


def test_reserving_the_same_book_twice_is_rejected(library):
    library.borrow_book("M001", ISBN)
    library.reserve_book("M002", ISBN)

    with pytest.raises(ValueError, match="already reserved"):
        library.reserve_book("M002", ISBN)


def test_reservation_by_an_unknown_member_is_rejected(library):
    library.borrow_book("M001", ISBN)

    with pytest.raises(LookupError, match="No member with id M404"):
        library.reserve_book("M404", ISBN)


def test_returning_a_reserved_book_notifies_the_first_member_in_line(library, notifier):
    library.borrow_book("M001", ISBN)
    library.reserve_book("M002", ISBN)

    library.return_book("M001", ISBN)

    notifier.notify_available.assert_called_once_with(library.get_member("M002"), library.get_book(ISBN))


def test_reservations_are_served_first_come_first_served(library, notifier):
    library.borrow_book("M001", ISBN)
    library.reserve_book("M002", ISBN)
    library.reserve_book("M003", ISBN)
    library.return_book("M001", ISBN)
    library.borrow_book("M002", ISBN)

    library.return_book("M002", ISBN)

    notifier.notify_available.assert_called_with(library.get_member("M003"), library.get_book(ISBN))


def test_copy_held_for_a_reserver_cannot_be_borrowed_by_someone_else(library):
    library.borrow_book("M001", ISBN)
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)

    with pytest.raises(ValueError, match="held for another member"):
        library.borrow_book("M003", ISBN)


def test_hold_is_released_once_the_reserver_borrows_the_copy(library):
    library.borrow_book("M001", ISBN)
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)
    library.borrow_book("M002", ISBN)
    library.return_book("M002", ISBN)

    library.borrow_book("M003", ISBN)

    assert library.get_member("M003").borrowed_books == [ISBN]


def test_book_whose_only_copy_is_held_can_still_be_reserved(library):
    library.borrow_book("M001", ISBN)
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)

    library.reserve_book("M003", ISBN)

    assert library.reservations_for(ISBN) == ["M003"]
