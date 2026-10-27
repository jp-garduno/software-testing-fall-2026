from datetime import date
import pytest
from src.book import Book
from src.member import Member
from src.library import Library

def make_book(isbn="1234567890", copies=1, title="Clean Code", author="Robert Martin"):
    return Book(isbn, title, author, copies=copies)

@pytest.fixture
def library():
    return Library()

def test_added_book_appears_in_available_books(library):
    book = make_book()
    library.add_book(book)
    assert library.get_available_books() == [book]

def test_available_books_excludes_books_without_copies(library):
    library.add_book(make_book("1234567890", copies=0))
    assert library.get_available_books() == []

def test_add_duplicate_isbn_raises(library):
    library.add_book(make_book())
    with pytest.raises(ValueError, match="already"):
        library.add_book(make_book())
