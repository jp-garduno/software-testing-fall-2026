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
