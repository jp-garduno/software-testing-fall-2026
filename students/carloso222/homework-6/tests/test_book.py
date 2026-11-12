import pytest

from src.book import Book
from src.exceptions import AllCopiesReturnedError, InvalidBookError, NoCopiesAvailableError


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


@pytest.mark.parametrize("title", ["", "   ", None])
def test_book_requires_a_title(title):
    with pytest.raises(InvalidBookError, match="Title"):
        Book("1234567890", title, "Author")


def test_book_title_is_trimmed():
    book = Book("1234567890", "  Test Book  ", "Author")
    assert book.title == "Test Book"


def test_book_rejects_negative_copies():
    with pytest.raises(InvalidBookError, match="negative"):
        Book("1234567890", "Test Book", "Author", total_copies=-1)


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", total_copies=1)
    assert book.is_available() is True


def test_book_is_not_available_when_it_has_zero_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=0)
    assert book.is_available() is False


def test_borrow_decreases_available_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=3)
    book.borrow()
    assert book.available_copies == 2


def test_borrow_does_not_change_total_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=3)
    book.borrow()
    assert book.total_copies == 3


def test_book_is_not_available_after_last_copy_is_borrowed():
    book = Book("1234567890", "Test Book", "Author", total_copies=1)
    book.borrow()
    assert book.is_available() is False


def test_borrow_raises_when_no_copies_are_available():
    book = Book("1234567890", "Test Book", "Author", total_copies=0)
    with pytest.raises(NoCopiesAvailableError):
        book.borrow()


def test_return_copy_increases_available_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    book.borrow()
    book.return_copy()
    assert book.available_copies == 2


def test_return_copy_raises_when_all_copies_are_already_in():
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    with pytest.raises(AllCopiesReturnedError):
        book.return_copy()


def test_book_stores_optional_genre_year_and_rating():
    book = Book("1234567890", "Test Book", "Author", genre="Fiction", year=1999, rating=4.5)
    assert (book.genre, book.year, book.rating) == ("Fiction", 1999, 4.5)


def test_book_repr_shows_isbn_and_title():
    book = Book("1234567890", "Test Book", "Author")
    assert repr(book) == "Book(isbn='1234567890', title='Test Book')"
