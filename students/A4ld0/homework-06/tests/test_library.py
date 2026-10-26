import pytest
from src.book import Book
from src.member import Member
from src.library import Library


def test_library_starts_empty():
    library = Library()
    assert (library.catalog, library.members) == ({}, {})


def test_add_book():
    library = Library()
    book = Book("1234567890", "Dune", "Frank Herbert")
    library.add_book(book)
    assert library.catalog[book.isbn] is book


def test_duplicate_isbn_preserves_catalog():
    library = Library()
    original = Book("1234567890", "Dune", "Frank Herbert")
    library.add_book(original)
    with pytest.raises(ValueError, match="ISBN"):
        library.add_book(Book(original.isbn, "Replacement", "Other"))
    assert library.catalog[original.isbn] is original
