"""Tests for the Library class."""

import pytest

from src.book import Book
from src.exceptions import BookNotFoundError
from src.library import Library


def test_added_book_can_be_found_by_isbn():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    library.add_book(book)
    assert library.get_book("1234567890") is book


def test_get_book_with_unknown_isbn_raises():
    with pytest.raises(BookNotFoundError):
        Library().get_book("1234567890")
