from book import Book
import pytest


def test_book_is_created_with_metadata():
    book = Book("1234567890", "TDD by Example", "Kent Beck")

    assert book.title == "TDD by Example"


@pytest.mark.parametrize("isbn", ["123", "123456789012", "not-an-isbn"])
def test_book_rejects_invalid_isbn(isbn):
    with pytest.raises(ValueError, match="ISBN"):
        Book(isbn, "Valid title", "Author")


def test_book_requires_title():
    with pytest.raises(ValueError, match="title"):
        Book("1234567890", "", "Author")


def test_book_is_available_when_copies_remain():
    assert Book("1234567890", "Book", "Author", 1).is_available() is True


def test_book_is_not_available_when_empty():
    assert Book("1234567890", "Book", "Author", 0).is_available() is False
