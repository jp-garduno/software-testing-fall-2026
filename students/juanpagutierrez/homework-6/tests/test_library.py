"""Tests for the Library class."""

from src.book import Book
from src.library import Library


def test_added_book_can_be_found_by_isbn():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    library.add_book(book)
    assert library.get_book("1234567890") is book
