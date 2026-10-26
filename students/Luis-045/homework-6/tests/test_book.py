

"""Behavioral tests for books."""

from src.book import Book


def test_book_stores_catalog_properties():
    book = Book("1234567890", "Dune", "Frank Herbert")
    assert (book.isbn, book.title, book.author) == (
        "1234567890", "Dune", "Frank Herbert"
    )


def test_book_initializes_total_and_available_copies():
    book = Book("1234567890", "Dune", "Frank Herbert", total_copies=2)
    assert (book.total_copies, book.available_copies) == (2, 2)
