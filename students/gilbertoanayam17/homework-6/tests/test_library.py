"""Tests for Library: catalog, members, borrowing, returning and searching."""

import pytest

from src import errors
from src.book import Book
from src.library import Library

ISBN = "1234567890"


def test_should_find_book_by_isbn_after_adding_it():
    library = Library()
    book = Book(ISBN, "Clean Code", "Robert C. Martin")

    library.add_book(book)

    assert library.get_book(ISBN) is book


def test_should_raise_error_when_book_is_not_in_catalog():
    with pytest.raises(errors.BookNotFoundError):
        Library().get_book(ISBN)
