from book import Book


def test_book_is_created_with_isbn_title_and_author():
    book = Book("0306406152", "Clean Code", "Robert Martin")

    assert (book.isbn, book.title, book.author) == ("0306406152", "Clean Code", "Robert Martin")
