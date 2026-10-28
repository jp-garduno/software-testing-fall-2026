import pytest
from src.book import Book


def test_book_creation_with_valid_attributes():
    book = Book(
        isbn="1234567890",
        title="The Pragmatic Programmer",
        author="Andy Hunt & Dave Thomas",
        total_copies=5,
    )
    assert book.isbn == "1234567890"
    assert book.title == "The Pragmatic Programmer"
    assert book.author == "Andy Hunt & Dave Thomas"
    assert book.total_copies == 5
    assert book.available_copies == 5


def test_book_creation_with_13_digit_isbn():
    book = Book("9780132350884", "Clean Code", "Robert C. Martin", 3)
    assert book.isbn == "9780132350884"


def test_book_creation_rejects_invalid_isbn_length():
    with pytest.raises(ValueError, match="ISBN must be 10 or 13 digits"):
        Book("123", "Invalid ISBN", "Author")


def test_book_creation_rejects_non_digit_isbn():
    with pytest.raises(ValueError, match="ISBN must be 10 or 13 digits"):
        Book("123456789X123", "Invalid ISBN", "Author")


def test_book_creation_rejects_empty_title():
    with pytest.raises(ValueError, match="Title is required"):
        Book("1234567890", "", "Author")


def test_book_creation_rejects_whitespace_title():
    with pytest.raises(ValueError, match="Title is required"):
        Book("1234567890", "   ", "Author")


def test_book_creation_rejects_negative_copies():
    with pytest.raises(ValueError, match="Total copies must be non-negative"):
        Book("1234567890", "Valid Title", "Author", total_copies=-1)


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=2)
    assert book.is_available() is True


def test_book_is_not_available_when_copies_are_zero():
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=0)
    assert book.is_available() is False


def test_book_borrow_decrements_available_copies():
    book = Book("1234567890", "Test-Driven Development", "Kent Beck", total_copies=2)
    book.borrow()
    assert book.available_copies == 1
    book.borrow()
    assert book.available_copies == 0


def test_book_borrow_raises_when_no_copies_available():
    book = Book("1234567890", "Test-Driven Development", "Kent Beck", total_copies=1)
    book.borrow()
    with pytest.raises(ValueError, match="No copies available to borrow"):
        book.borrow()


def test_book_return_copy_increments_available_copies():
    book = Book("1234567890", "Test-Driven Development", "Kent Beck", total_copies=2)
    book.borrow()
    assert book.available_copies == 1
    book.return_copy()
    assert book.available_copies == 2


def test_book_return_copy_raises_when_all_copies_already_returned():
    book = Book("1234567890", "Test-Driven Development", "Kent Beck", total_copies=2)
    with pytest.raises(ValueError, match="Cannot return more copies than total copies"):
        book.return_copy()


def test_book_string_representation_and_equality():
    book1 = Book("1234567890", "Clean Code", "Robert C. Martin")
    book2 = Book("1234567890", "Clean Code", "Robert C. Martin")
    assert repr(book1) == "<Book ISBN=1234567890 Title='Clean Code'>"
    assert book1 == book2
    assert book1 != "not-a-book"
