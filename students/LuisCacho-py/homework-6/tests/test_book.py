import pytest
from src.book import Book


def test_book_can_be_created_with_properties():
    book = Book("1234567890", "Clean Code", "Robert C. Martin")
    assert book.isbn == "1234567890"
    assert book.title == "Clean Code"
    assert book.author == "Robert C. Martin"
    assert book.total_copies == 1
    assert book.available_copies == 1


def test_book_can_be_created_with_multiple_copies():
    book = Book("9780132350884", "The Pragmatic Programmer", "Andy Hunt", total_copies=5)
    assert book.total_copies == 5
    assert book.available_copies == 5
