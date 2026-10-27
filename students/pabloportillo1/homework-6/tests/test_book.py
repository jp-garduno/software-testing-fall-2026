from book import Book


def test_book_is_created_with_isbn_title_and_author():
    book = Book("0306406152", "Clean Code", "Robert Martin")

    assert (book.isbn, book.title, book.author) == ("0306406152", "Clean Code", "Robert Martin")


def test_book_starts_with_all_copies_available():
    book = Book("0306406152", "Clean Code", "Robert Martin", total_copies=5)

    assert book.available_copies == 5


def test_book_with_copies_is_available():
    book = Book("0306406152", "Clean Code", "Robert Martin", total_copies=1)

    assert book.is_available() is True
