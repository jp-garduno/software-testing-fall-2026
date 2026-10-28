import pytest
from src.book import Book


def test_book_creation_with_valid_attributes():
    book = Book(
        isbn="1234567890",
        title="The Pragmatic Programmer",
        author="Andy Hunt & Dave Thomas",
        total_copies=5,
    )
    assert book.isbn == "1234567890"
    assert book.title == "The Pragmatic Programmer"
    assert book.author == "Andy Hunt & Dave Thomas"
    assert book.total_copies == 5
    assert book.available_copies == 5
