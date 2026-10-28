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


@pytest.mark.parametrize("title", ["", "  ", None, 42])
def test_book_requires_a_title(title):
    with pytest.raises(ValueError, match="title"):
        Book("1234567890123", title, "Author")


@pytest.mark.parametrize("copies", [-1, 1.5, True, "2"])
def test_book_rejects_invalid_copy_counts(copies):
    with pytest.raises(ValueError, match="copies"):
        Book("1234567890", "Title", "Author", copies)


@pytest.mark.parametrize("copies, expected", [(0, False), (1, True)])
def test_book_availability_depends_on_stock(copies, expected):
    assert Book("1234567890", "Title", "Author", copies).is_available() is expected


def test_borrow_removes_one_available_copy():
    book = Book("1234567890", "Title", "Author", 2)
    book.borrow()
    assert book.available_copies == 1


def test_borrow_rejects_exhausted_stock():
    book = Book("1234567890", "Title", "Author", 0)
    with pytest.raises(ValueError, match="available"):
        book.borrow()
    assert book.available_copies == 0
