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
