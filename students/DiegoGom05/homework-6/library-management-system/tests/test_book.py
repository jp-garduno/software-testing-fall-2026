from src.book import Book

def test_book_can_be_created():
    book = Book("1234567890", "Test Book", "Author")
    assert book.title == "Test Book"

def test_book_stores_isbn_and_author():
    book = Book("1234567890", "Test Book", "Author")
    assert (book.isbn, book.author) == ("1234567890", "Author")
