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


def test_book_rejects_empty_title():
    with pytest.raises(ValueError, match="Title is required"):
        Book("1234567890", "", "Author")


def test_book_rejects_empty_author():
    with pytest.raises(ValueError, match="Author is required"):
        Book("1234567890", "Title", "")


def test_book_rejects_invalid_isbn_length():
    with pytest.raises(ValueError, match="ISBN must be 10 or 13 digits"):
        Book("12345", "Title", "Author")


def test_book_rejects_non_digit_isbn():
    with pytest.raises(ValueError, match="ISBN must be 10 or 13 digits"):
        Book("123456789X123", "Title", "Author")


def test_book_rejects_negative_copies():
    with pytest.raises(ValueError, match="Total copies cannot be negative"):
        Book("1234567890", "Title", "Author", total_copies=-1)


def test_book_accepts_isbn_with_hyphens():
    book = Book("978-0-13-235088-4", "Clean Code", "Robert C. Martin")
    assert book.isbn == "9780132350884"


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=2)
    assert book.is_available() is True


def test_book_is_not_available_when_zero_copies():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=0)
    assert book.is_available() is False
