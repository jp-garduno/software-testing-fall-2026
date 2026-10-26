import pytest
from src.book import Book


def test_book_identifying_properties():
    book = Book("1234567890", "Dune", "Frank Herbert")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Dune", "Frank Herbert")
