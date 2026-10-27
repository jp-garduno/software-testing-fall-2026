import pytest

from book import Book
from library import Library
from member import Member

ISBN = "0306406152"


@pytest.fixture(name="library")
def fixture_library(clock):
    library = Library(clock=clock)
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
