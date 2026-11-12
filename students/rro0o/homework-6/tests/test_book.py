"""Tests for the Book class."""
# pylint: disable=missing-function-docstring

import pytest

from src.book import Book
from src.errors import LibraryError


def test_book_can_be_created_with_isbn_title_and_author():
    book = Book("1234567890", "Test Book", "Author")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Test Book", "Author")


def test_book_has_one_copy_by_default():
    assert Book("1234567890", "Test Book", "Author").available_copies == 1


def test_book_has_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=5)
    assert (book.total_copies, book.available_copies) == (5, 5)


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() is True


def test_book_is_not_available_when_no_copies():
    book = Book("1234567890", "Test Book", "Author", copies=0)
    assert book.is_available() is False


def test_isbn_with_nine_digits_is_rejected():
    with pytest.raises(ValueError):
        Book("123456789", "Test Book", "Author")


def test_isbn_with_letters_is_rejected():
    with pytest.raises(ValueError):
        Book("12345abcde", "Test Book", "Author")


def test_isbn_with_thirteen_digits_is_accepted():
    assert Book("1234567890123", "Test Book", "Author").isbn == "1234567890123"


@pytest.mark.parametrize("title", ["", "   "])
def test_blank_title_is_rejected(title):
    with pytest.raises(ValueError):
        Book("1234567890", title, "Author")


def test_negative_copies_are_rejected():
    with pytest.raises(ValueError):
        Book("1234567890", "Test Book", "Author", copies=-1)


def test_borrow_decreases_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=2)
    book.borrow()
    assert book.available_copies == 1


def test_borrow_without_copies_raises_error():
    book = Book("1234567890", "Test Book", "Author", copies=0)
    with pytest.raises(LibraryError):
        book.borrow()


def test_return_copy_increases_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=2)
    book.borrow()
    book.return_copy()
    assert book.available_copies == 2


def test_return_copy_beyond_total_raises_error():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    with pytest.raises(LibraryError):
        book.return_copy()
