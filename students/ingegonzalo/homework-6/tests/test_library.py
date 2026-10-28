import pytest

from src.book import Book
from src.library import Library
from src.member import Member

def test_new_library_has_no_available_books():
    library = Library()
    assert library.get_available_books() == []

def test_add_book_makes_it_available_in_catalog():
    library = Library()
    book = Book("1234567890", "Test Book", "Author")
    library.add_book(book)
    assert library.get_available_books() == [book]