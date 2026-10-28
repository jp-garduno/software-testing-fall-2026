import pytest

from src.book import Book


def test_book_records_bibliographic_properties():
    book = Book("1234567890", "Pedro Paramo", "Juan Rulfo")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Pedro Paramo", "Juan Rulfo")
