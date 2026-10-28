import pytest

from book import Book
from library import Library

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
