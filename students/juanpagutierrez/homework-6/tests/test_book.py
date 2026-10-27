"""Tests for the Book class."""

import pytest

from src.book import Book
from src.exceptions import BookUnavailableError


def test_book_can_be_created_with_isbn_title_and_author():
    book = Book("1234567890", "Clean Code", "Robert Martin")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Clean Code", "Robert Martin")


def test_book_starts_with_all_copies_available():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=5)
    assert book.available_copies == 5


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=1)
    assert book.is_available() is True


def test_book_is_not_available_when_no_copies():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=0)
    assert book.is_available() is False


def test_borrow_decrements_available_copies():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=2)
    book.borrow()
    assert book.available_copies == 1


def test_borrow_raises_when_no_copies_available():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=0)
    with pytest.raises(BookUnavailableError):
        book.borrow()


def test_return_copy_increments_available_copies():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=1)
    book.borrow()
    book.return_copy()
    assert book.available_copies == 1


def test_return_copy_raises_when_all_copies_are_already_in():
    book = Book("1234567890", "Clean Code", "Robert Martin", total_copies=1)
    with pytest.raises(ValueError):
        book.return_copy()


@pytest.mark.parametrize("isbn", ["123", "12345678901", "123456789012345"])
def test_isbn_with_wrong_length_is_rejected(isbn):
    with pytest.raises(ValueError):
        Book(isbn, "Clean Code", "Robert Martin")


def test_isbn_with_non_digit_characters_is_rejected():
    with pytest.raises(ValueError):
        Book("123456789X", "Clean Code", "Robert Martin")
