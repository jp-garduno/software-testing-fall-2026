from src.book import Book
import pytest


def test_book_can_be_created():
    book = Book("1234567890", "Test Book", "Author")
    assert book.title == "Test Book"

def test_book_has_available_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=5)
    assert book.available_copies == 5

def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", total_copies=1)
    assert book.is_available() is True

def test_book_is_not_available_when_no_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=0)
    assert book.is_available() is False

def test_book_has_total_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=5)
    assert book.total_copies == 5

def test_book_rejects_isbn_with_invalid_length():
    with pytest.raises(ValueError):
        Book("12345", "Test Book", "Author")

def test_book_rejects_isbn_with_non_digits():
    with pytest.raises(ValueError):
        Book("12345abcde", "Test Book", "Author")

def test_book_requires_title():
    with pytest.raises(ValueError):
        Book("1234567890", "", "Author")