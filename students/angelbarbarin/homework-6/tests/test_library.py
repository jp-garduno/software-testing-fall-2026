import pytest

from book import Book
from exceptions import (
    AlreadyBorrowedError,
    BookNotFoundError,
    BorrowLimitExceededError,
    MemberNotFoundError,
)
from library import Library
from member import Member

ISBN = "0306406152"


def test_add_book_makes_it_findable_by_isbn():
    library = Library()
    book = Book(ISBN, "Clean Code", "Robert C. Martin")
    library.add_book(book)
    assert library.get_book(ISBN) is book


def test_register_member_makes_it_findable_by_id():
    library = Library()
    member = Member("M001", "Ana Lopez")
    library.register_member(member)
    assert library.get_member("M001") is member


def test_borrow_book_assigns_copy_to_member(library):
    library.borrow_book("M001", ISBN)
    assert library.get_member("M001").borrowed_books == [ISBN]


def test_borrow_book_raises_for_unknown_member(library):
    with pytest.raises(MemberNotFoundError):
        library.borrow_book("M999", ISBN)


def test_borrow_book_raises_for_unknown_isbn(library):
    with pytest.raises(BookNotFoundError):
        library.borrow_book("M001", "9999999999")


def test_borrow_book_keeps_copy_when_member_reached_limit(library):
    library.register_member(Member("M002", "Luis Perez", max_borrow_limit=0))
    with pytest.raises(BorrowLimitExceededError):
        library.borrow_book("M002", ISBN)
    assert library.get_book(ISBN).available_copies == 2


def test_return_book_restores_copy(library):
    library.borrow_book("M001", ISBN)
    library.return_book("M001", ISBN)
    assert library.get_book(ISBN).available_copies == 2


@pytest.fixture
def catalog():
    lib = Library()
    lib.add_book(Book("0306406152", "Clean Code", "Robert C. Martin"))
    lib.add_book(Book("9780132350884", "The Clean Coder", "Robert C. Martin"))
    lib.add_book(Book("9780201633610", "Design Patterns", "Erich Gamma", 0))
    return lib


def test_search_by_title_is_partial_and_case_insensitive(catalog):
    titles = [book.title for book in catalog.search_by_title("clean")]
    assert titles == ["Clean Code", "The Clean Coder"]


def test_search_by_author_is_partial_and_case_insensitive(catalog):
    titles = [book.title for book in catalog.search_by_author("gamma")]
    assert titles == ["Design Patterns"]


def test_get_available_books_excludes_books_without_copies(catalog):
    titles = [book.title for book in catalog.get_available_books()]
    assert titles == ["Clean Code", "The Clean Coder"]


def test_borrow_book_rejects_same_book_twice_for_member(library):
    library.borrow_book("M001", ISBN)
    with pytest.raises(AlreadyBorrowedError):
        library.borrow_book("M001", ISBN)
