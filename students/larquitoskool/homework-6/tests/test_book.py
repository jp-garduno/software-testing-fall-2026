import pytest
from book import Book

def test_book_creation():
    book = Book("1234567890", "TDD", "Author")
    assert book.title == "TDD"

def test_book_invalid_isbn():
    with pytest.raises(ValueError, match="ISBN must be 10 or 13 digits"):
        Book("123", "Title", "Author")

def test_book_missing_title():
    with pytest.raises(ValueError, match="Title is required"):
        Book("1234567890", "", "Author")

def test_book_is_available():
    assert Book("1234567890", "TDD", "Author", 1).is_available()

def test_book_not_available():
    assert not Book("1234567890", "TDD", "Author", 0).is_available()

def test_borrow_book():
    book = Book("1234567890", "TDD", "Author", 1)
    book.borrow()
    assert book.available_copies == 0

def test_borrow_unavailable_raises_error():
    with pytest.raises(ValueError, match="Book is not available"):
        Book("1234567890", "TDD", "Author", 0).borrow()

def test_return_book():
    book = Book("1234567890", "TDD", "Author", 1)
    book.borrow()
    book.return_copy()
    assert book.available_copies == 1

def test_return_extra_raises_error():
    with pytest.raises(ValueError, match="All copies returned"):
        Book("1234567890", "TDD", "Author", 1).return_copy()