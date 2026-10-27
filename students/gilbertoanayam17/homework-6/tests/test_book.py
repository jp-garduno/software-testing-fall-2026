"""Tests for Book: catalog data, copy tracking and validation."""

import pytest

from src import errors
from src.book import Book


ISBN = "1234567890"


def make_book(copies=1):
    """Arrange a valid book; only the number of copies changes between tests."""
    return Book(ISBN, "Clean Code", "Robert C. Martin", copies=copies)


def test_should_store_isbn_title_and_author_when_created():
    book = Book(ISBN, "Clean Code", "Robert C. Martin")

    assert (book.isbn, book.title, book.author) == (ISBN, "Clean Code", "Robert C. Martin")


def test_should_track_available_copies_when_created_with_copies():
    assert make_book(copies=5).available_copies == 5


def test_should_be_available_when_copies_exist():
    assert make_book(copies=1).is_available()


def test_should_not_be_available_when_no_copies_exist():
    assert not make_book(copies=0).is_available()


def test_should_decrease_available_copies_when_borrowed():
    book = make_book(copies=2)

    book.borrow()

    assert book.available_copies == 1


def test_should_raise_error_when_borrowing_unavailable_book():
    book = make_book(copies=0)

    with pytest.raises(errors.BookNotAvailableError):
        book.borrow()
