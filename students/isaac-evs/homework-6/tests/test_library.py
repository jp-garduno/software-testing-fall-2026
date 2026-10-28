import pytest

from book import Book
from library import Library
from member import Member

ISBN = "1234567890"
OTHER_ISBN = "0987654321"


@pytest.fixture
def library():
    return Library()


def test_added_book_is_listed_as_available(library):
    book = Book(ISBN, "Test Book", "Author")
    library.add_book(book)
    assert library.get_available_books() == [book]


def test_available_books_excludes_books_without_copies(library):
    available = Book(ISBN, "Available", "Author", copies=1)
    gone = Book(OTHER_ISBN, "Gone", "Author", copies=0)
    library.add_book(available)
    library.add_book(gone)
    assert library.get_available_books() == [available]


def test_registered_member_can_be_found(library):
    member = Member("m1", "Alice")
    library.register_member(member)
    assert library.get_member("m1") is member


def test_borrow_book_takes_a_copy(library):
    book = Book(ISBN, "Test Book", "Author", copies=1)
    library.add_book(book)
    library.register_member(Member("m1", "Alice"))
    library.borrow_book("m1", ISBN)
    assert book.available_copies == 0


def test_borrow_book_fails_for_unknown_member(library):
    library.add_book(Book(ISBN, "Test Book", "Author"))
    with pytest.raises(ValueError, match="Member not found"):
        library.borrow_book("ghost", ISBN)
