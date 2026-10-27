import pytest
from src.book import Book


@pytest.fixture
def book():
    return Book("1234567890", "Test Book", "Author")


def test_book_can_be_created(book):
    assert book.title == "Test Book"


def test_book_stores_isbn_and_author(book):
    assert (book.isbn, book.author) == ("1234567890", "Author")


def test_book_has_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=5)
    assert book.available_copies == 5


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() is True


def test_book_not_available_when_no_copies():
    book = Book("1234567890", "Test Book", "Author", copies=0)
    assert book.is_available() is False

def test_borrow_decreases_available_copies():
    book = Book("1234567890", "T", "A", copies=2)
    book.borrow()
    assert book.available_copies == 1

def test_borrow_raises_when_no_copies():
    book = Book("1234567890", "T", "A", copies=0)
    with pytest.raises(ValueError, match="No copies available"):
        book.borrow()

def test_return_copy_increases_available_copies():
    book = Book("1234567890", "T", "A", copies=1)
    book.borrow()
    book.return_copy()
    assert book.available_copies == 1

def test_return_copy_cannot_exceed_total_copies():
    book = Book("1234567890", "T", "A", copies=1)
    with pytest.raises(ValueError):
        book.return_copy()

def test_isbn_rejects_invalid_length():
    with pytest.raises(ValueError):
        Book("123456789", "T", "A")        # 9 dígitos
