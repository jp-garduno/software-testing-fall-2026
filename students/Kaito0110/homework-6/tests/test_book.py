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


def test_book_rejects_invalid_isbn_length():
    with pytest.raises(ValueError):
        Book(
            isbn="12345",
            title="Clean Code",
            author="Robert C. Martin",
            total_copies=3,
            available_copies=3,
        )


def test_book_rejects_empty_title():
    with pytest.raises(ValueError):
        Book(
            isbn="9780132350884",
            title="",
            author="Robert C. Martin",
            total_copies=3,
            available_copies=3,
        )


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


def test_return_copy_does_not_change_count_when_all_copies_are_available():
    book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        total_copies=3,
        available_copies=3,
    )

    book.return_copy()

    assert book.available_copies == 3


def test_book_rejects_isbn_with_letters():
    with pytest.raises(ValueError):
        Book(
            isbn="97801323508AB",
            title="Clean Code",
            author="Robert C. Martin",
            total_copies=3,
            available_copies=3,
        )


def test_book_rejects_title_with_only_spaces():
    with pytest.raises(ValueError):
        Book(
            isbn="9780132350884",
            title="   ",
            author="Robert C. Martin",
            total_copies=3,
            available_copies=3,
        )


def test_book_rejects_more_available_copies_than_total():
    with pytest.raises(ValueError):
        Book(
            isbn="9780132350884",
            title="Clean Code",
            author="Robert C. Martin",
            total_copies=3,
            available_copies=4,
        )


def test_book_rejects_negative_available_copies():
    with pytest.raises(ValueError):
        Book(
            isbn="9780132350884",
            title="Clean Code",
            author="Robert C. Martin",
            total_copies=3,
            available_copies=-1,
        )


def test_book_rejects_negative_total_copies():
    with pytest.raises(
        ValueError,
        match="Total copies cannot be negative",
    ):
        Book(
            isbn="9780132350884",
            title="Clean Code",
            author="Robert C. Martin",
            total_copies=-1,
            available_copies=0,
        )


def test_book_defaults_available_copies_to_total_copies():
    book = Book(
        isbn="1234567890",
        title="Refactoring",
        author="Martin Fowler",
        total_copies=4,
    )

    assert book.available_copies == 4


