from src.book import Book


def test_book_can_be_created_with_isbn_title_and_author():
    book = Book("1234567890", "Test Book", "Author")
    assert (book.isbn, book.title, book.author) == ("1234567890", "Test Book", "Author")


def test_book_has_one_copy_by_default():
    book = Book("1234567890", "Test Book", "Author")
    assert book.total_copies == 1


def test_new_book_has_all_copies_available():
    book = Book("1234567890", "Test Book", "Author", total_copies=5)
    assert book.available_copies == 5


def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", total_copies=1)
    assert book.is_available() is True


def test_book_is_not_available_when_it_has_zero_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=0)
    assert book.is_available() is False
