import pytest

from book import Book

ISBN = "0306406152"


def make_book(total_copies=1):
    return Book(ISBN, "Clean Code", "Robert Martin", total_copies=total_copies)


def test_book_is_created_with_isbn_title_and_author():
    book = make_book()

    assert (book.isbn, book.title, book.author) == (ISBN, "Clean Code", "Robert Martin")


def test_book_starts_with_all_copies_available():
    assert make_book(total_copies=5).available_copies == 5


def test_book_with_copies_is_available():
    assert make_book(total_copies=1).is_available() is True


def test_book_without_copies_is_not_available():
    assert make_book(total_copies=0).is_available() is False


def test_borrow_takes_one_copy():
    book = make_book(total_copies=2)

    book.borrow()

    assert book.available_copies == 1


def test_borrow_without_available_copies_is_rejected():
    book = make_book(total_copies=0)

    with pytest.raises(ValueError, match="No copies available"):
        book.borrow()


def test_return_copy_puts_the_copy_back():
    book = make_book(total_copies=2)
    book.borrow()

    book.return_copy()

    assert book.available_copies == 2


def test_return_copy_when_every_copy_is_in_is_rejected():
    book = make_book(total_copies=2)

    with pytest.raises(ValueError, match="All copies .* already in"):
        book.return_copy()


def test_isbn_with_nine_digits_is_rejected():
    with pytest.raises(ValueError, match="ISBN must be 10 or 13 digits"):
        Book("030640615", "Clean Code", "Robert Martin")


def test_isbn_with_thirteen_digits_is_accepted():
    assert Book("9780306406157", "Clean Code", "Robert Martin").isbn == "9780306406157"


def test_isbn_with_a_letter_is_rejected():
    with pytest.raises(ValueError, match="ISBN must be 10 or 13 digits"):
        Book("03064O6152", "Clean Code", "Robert Martin")


@pytest.mark.parametrize("title", ["", "   "])
def test_blank_title_is_rejected(title):
    with pytest.raises(ValueError, match="Title is required"):
        Book(ISBN, title, "Robert Martin")
