import pytest
from src.book import Book


def test_book_identifying_properties():
    book = Book("1234567890", "Dune", "Frank Herbert")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Dune", "Frank Herbert")


def test_book_initial_copies():
    book = Book("1234567890", "Dune", "Herbert", total_copies=2)
    assert (book.total_copies, book.available_copies) == (2, 2)


@pytest.mark.parametrize("copies, expected", [(0, False), (1, True)])
def test_book_availability(copies, expected):
    assert Book("1234567890", "Dune", "Herbert", copies).is_available() is expected


def test_borrow_decrements_copies():
    book = Book("1234567890", "Dune", "Herbert", 2)
    book.borrow()
    assert book.available_copies == 1


def test_borrow_unavailable_book():
    book = Book("1234567890", "Dune", "Herbert", 0)
    with pytest.raises(ValueError, match="available"):
        book.borrow()
    assert book.available_copies == 0


def test_return_copy_restores_availability():
    book = Book("1234567890", "Dune", "Herbert")
    book.borrow()
    book.return_copy()
    assert book.available_copies == book.total_copies


def test_return_without_borrow():
    book = Book("1234567890", "Dune", "Herbert")
    with pytest.raises(ValueError, match="return"):
        book.return_copy()
    assert book.available_copies == 1


@pytest.mark.parametrize("isbn", ["", "123", "12345678901", "12345678901234"])
def test_reject_invalid_isbn_length(isbn):
    with pytest.raises(ValueError, match="ISBN"):
        Book(isbn, "Dune", "Herbert")
