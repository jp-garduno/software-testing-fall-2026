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
