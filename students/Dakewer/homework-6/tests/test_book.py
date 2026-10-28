import pytest

from src.book import Book


def test_book_can_be_created():
    book = Book("1234567890", "Test Book", "Author")
    assert book.title == "Test Book"


def test_book_has_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=5)
    assert book.available_copies == 5


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() is True


def test_book_not_available_when_no_copies():
    book = Book("1234567890", "Test", "Author", copies=0)
    assert book.is_available() is False


def test_book_tracks_total_copies():
    book = Book("1234567890", "Test Book", "Author", copies=5)
    assert book.total_copies == 5


def test_book_rejects_isbn_with_wrong_length():
    with pytest.raises(ValueError):
        Book("12345", "Test Book", "Author")


def test_book_accepts_13_digit_isbn():
    book = Book("1234567890123", "Test Book", "Author")
    assert book.isbn == "1234567890123"


def test_book_rejects_isbn_with_non_digits():
    with pytest.raises(ValueError):
        Book("12345abcde", "Test Book", "Author")


def test_book_requires_title():
    with pytest.raises(ValueError):
        Book("1234567890", "", "Author")


def test_book_rejects_whitespace_only_title():
    with pytest.raises(ValueError):
        Book("1234567890", "   ", "Author")


def test_book_rejects_negative_copies():
    with pytest.raises(ValueError):
        Book("1234567890", "Test Book", "Author", copies=-1)


def test_borrow_decreases_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=2)
    book.borrow()
    assert book.available_copies == 1


def test_borrow_fails_when_no_copies_available():
    book = Book("1234567890", "Test Book", "Author", copies=0)
    with pytest.raises(ValueError):
        book.borrow()


def test_return_copy_increases_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=2)
    book.borrow()
    book.return_copy()
    assert book.available_copies == 2


def test_return_copy_cannot_exceed_total_copies():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    with pytest.raises(ValueError):
        book.return_copy()
