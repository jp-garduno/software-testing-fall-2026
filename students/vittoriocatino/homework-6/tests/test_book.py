from book import Book


def test_book_is_created_with_metadata():
    book = Book("1234567890", "TDD by Example", "Kent Beck")

    assert book.title == "TDD by Example"
