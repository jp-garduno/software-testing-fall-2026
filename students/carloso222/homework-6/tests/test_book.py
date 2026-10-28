import pytest

from src.book import Book
from src.exceptions import InvalidBookError


def test_book_can_be_created_with_isbn_title_and_author():
    book = Book("1234567890", "Test Book", "Author")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Test Book", "Author")


def test_book_has_one_copy_by_default():
    book = Book("1234567890", "Test Book", "Author")
    assert book.total_copies == 1


def test_new_book_has_all_copies_available():
    book = Book("1234567890", "Test Book", "Author", total_copies=5)
    assert book.available_copies == 5


def test_book_accepts_13_digit_isbn():
    book = Book("9780132350884", "Clean Code", "Robert C. Martin")
    assert book.isbn == "9780132350884"


@pytest.mark.parametrize("isbn", ["123456789", "12345678901", "123456789012", "12345678901234"])
def test_book_rejects_isbn_with_wrong_length(isbn):
    with pytest.raises(InvalidBookError, match="10 or 13"):
        Book(isbn, "Test Book", "Author")


@pytest.mark.parametrize("isbn", ["12345ABCDE", "123-456-789", "", None, 1234567890])
def test_book_rejects_isbn_that_is_not_a_digit_string(isbn):
    with pytest.raises(InvalidBookError, match="digits"):
        Book(isbn, "Test Book", "Author")


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", total_copies=1)
    assert book.is_available() is True


def test_book_is_not_available_when_it_has_zero_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=0)
    assert book.is_available() is False
