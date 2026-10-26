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
