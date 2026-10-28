from book import Book


def test_book_can_be_created():
    book = Book("1234567890", "Test Book", "Author")
    assert book.title == "Test Book"


def test_book_has_available_copies():
    book = Book("1234567890", "Test Book", "Author", copies=5)
    assert book.available_copies == 5
