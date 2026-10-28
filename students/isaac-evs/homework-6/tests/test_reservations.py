import pytest

from book import Book
from library import Library
from member import Member

ISBN = "1234567890"
OTHER_ISBN = "0987654321"


@pytest.fixture
def library():
    lib = Library()
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
