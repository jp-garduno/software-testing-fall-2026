"""Unit tests for the Book class developed with TDD."""

import pytest
from src.book import Book


def test_book_is_available_when_copies_exist():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=3,
    )

    assert book.is_available() is True


def test_book_is_not_available_when_no_copies_exist():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=0,
    )

    assert book.is_available() is False


def test_return_copy_increases_available_copies():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=2,
    )

    book.return_copy()

    assert book.available_copies == 3


def test_return_copy_does_not_exceed_total_copies():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=3,
    )

    book.return_copy()

    assert book.available_copies == 3


def test_borrow_reduces_available_copies():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=3,
    )

    book.borrow()

    assert book.available_copies == 2


def test_borrow_raises_error_when_no_copies_are_available():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=0,
    )

    with pytest.raises(ValueError):
        book.borrow()

    assert book.available_copies == 0
