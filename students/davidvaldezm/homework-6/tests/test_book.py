import pytest

from src.book import Book


def test_book_records_bibliographic_properties():
    book = Book("1234567890", "Pedro Paramo", "Juan Rulfo")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Pedro Paramo", "Juan Rulfo")


def test_book_starts_with_requested_copies():
    book = Book("1234567890", "Pedro Paramo", "Juan Rulfo", copies=3)
    assert (book.total_copies, book.available_copies) == (3, 3)


@pytest.mark.parametrize("isbn", ["123", "123456789X", "1" * 11, 1234567890, None, "Ù¡Ù¢Ù£Ù¤Ù¥Ù¦Ù§Ù¨Ù©Ù "])
def test_book_rejects_invalid_isbn(isbn):
    with pytest.raises(ValueError, match="ISBN"):
        Book(isbn, "Title", "Author")
