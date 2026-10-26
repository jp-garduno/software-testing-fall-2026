"""Behavioral tests for books."""

import pytest

from src.book import Book


def test_book_stores_catalog_properties():
    book = Book("1234567890", "Dune", "Frank Herbert")
    assert (book.isbn, book.title, book.author) == (
        "1234567890",
        "Dune",
        "Frank Herbert",
    )


def test_book_initializes_total_and_available_copies():
    book = Book("1234567890", "Dune", "Frank Herbert", total_copies=2)
    assert (book.total_copies, book.available_copies) == (2, 2)


def test_book_rejects_an_isbn_with_wrong_length():
    with pytest.raises(ValueError, match="ISBN"):
        Book("123", "Dune", "Frank Herbert")


def test_book_rejects_an_isbn_containing_letters():
    with pytest.raises(ValueError, match="ISBN"):
        Book("123456789X", "Dune", "Frank Herbert")


def test_book_rejects_an_empty_title():
    with pytest.raises(ValueError, match="title"):
        Book("1234567890", "", "Frank Herbert")


def test_book_rejects_a_whitespace_title():
    with pytest.raises(ValueError, match="title"):
        Book("1234567890", "   ", "Frank Herbert")


def test_book_with_no_copies_is_unavailable():
    book = Book("1234567890", "Dune", "Frank Herbert", total_copies=0)
    assert book.is_available() is False


def test_book_with_copies_is_available():
    assert Book("1234567890", "Dune", "Frank Herbert").is_available() is True


def test_borrow_decreases_available_copies():
    book = Book("1234567890", "Dune", "Frank Herbert", total_copies=2)
    book.borrow()
    assert book.available_copies == 1


def test_borrow_rejects_an_unavailable_book():
    book = Book("1234567890", "Dune", "Frank Herbert", total_copies=0)
    with pytest.raises(ValueError, match="available"):
        book.borrow()


def test_return_copy_restores_available_inventory():
    book = Book("1234567890", "Dune", "Frank Herbert")
    book.borrow()
    book.return_copy()
    assert book.available_copies == 1


def test_return_copy_rejects_an_extra_copy():
    book = Book("1234567890", "Dune", "Frank Herbert")
    with pytest.raises(ValueError, match="borrowed"):
        book.return_copy()


def test_book_rejects_negative_inventory():
    with pytest.raises(ValueError, match="copies"):
        Book("1234567890", "Dune", "Frank Herbert", total_copies=-1)


def test_book_accepts_a_thirteen_digit_isbn():
    assert Book("9780441172719", "Dune", "Frank Herbert").isbn == "9780441172719"


def test_book_stores_search_metadata():
    book = Book(
        "1234567890",
        "Dune",
        "Frank Herbert",
        genre="Science Fiction",
        publication_year=1965,
        rating=4.8,
    )
    assert book.metadata == {
        "genre": "Science Fiction",
        "publication_year": 1965,
        "rating": 4.8,
    }


def test_book_rejects_fractional_inventory():
    with pytest.raises(ValueError, match="copies"):
        Book("1234567890", "Dune", "Frank Herbert", total_copies=1.5)


def test_book_rejects_boolean_inventory():
    with pytest.raises(ValueError, match="copies"):
        Book("1234567890", "Dune", "Frank Herbert", total_copies=True)


def test_book_rejects_a_nonstring_isbn_with_a_validation_error():
    with pytest.raises(ValueError, match="ISBN"):
        Book(1234567890, "Dune", "Frank Herbert")


def test_book_rejects_non_ascii_isbn_digits():
    with pytest.raises(ValueError, match="ISBN"):
        Book("１２３４５６７８９０", "Dune", "Frank Herbert")
