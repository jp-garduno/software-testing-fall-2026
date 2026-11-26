"""Tests for Library: catalog, members, borrowing, returning and searching."""

import pytest

from src import errors
from src.book import Book
from src.library import Library
from src.member import Member

ISBN = "1234567890"

def make_library(copies=1, limit=3):
    """Arrange a library with one book and one registered member, M1."""
    library = Library()
    library.add_book(Book(ISBN, "Clean Code", "Robert C. Martin", copies=copies))
    library.register_member(Member("M1", "Ana Lopez", max_borrow_limit=limit))
    return library


def test_should_find_book_by_isbn_after_adding_it():
    library = Library()
    book = Book(ISBN, "Clean Code", "Robert C. Martin")

    library.add_book(book)

    assert library.get_book(ISBN) is book


def test_should_raise_error_when_book_is_not_in_catalog():
    with pytest.raises(errors.BookNotFoundError):
        Library().get_book(ISBN)


def test_should_find_member_by_id_after_registering_them():
    library = Library()
    member = Member("M1", "Ana Lopez")

    library.register_member(member)

    assert library.get_member("M1") is member


def test_should_raise_error_when_member_is_not_registered():
    with pytest.raises(errors.MemberNotFoundError):
        Library().get_member("M404")


def test_should_record_book_on_member_when_borrowed():
    library = make_library()

    library.borrow_book("M1", ISBN)

    assert library.get_member("M1").borrowed_books == [ISBN]


def test_should_take_copy_off_shelf_when_borrowed():
    library = make_library(copies=1)

    library.borrow_book("M1", ISBN)

    assert library.get_book(ISBN).available_copies == 0


def test_should_keep_copy_on_shelf_when_member_is_at_limit():
    library = make_library(copies=2, limit=1)
    library.borrow_book("M1", ISBN)

    with pytest.raises(errors.BorrowLimitExceededError):
        library.borrow_book("M1", ISBN)

    assert library.get_book(ISBN).available_copies == 1


def test_should_put_copy_back_on_shelf_when_returned():
    library = make_library(copies=1)
    library.borrow_book("M1", ISBN)

    library.return_book("M1", ISBN)

    assert library.get_book(ISBN).available_copies == 1


def test_should_remove_book_from_member_when_returned():
    library = make_library()
    library.borrow_book("M1", ISBN)

    library.return_book("M1", ISBN)

    assert not library.get_member("M1").borrowed_books


def test_should_find_books_by_partial_title_ignoring_case():
    library = make_library()
    library.add_book(Book("9780135957059", "The Pragmatic Programmer", "David Thomas"))

    found = library.search_by_title("clean")

    assert [book.isbn for book in found] == [ISBN]


def test_should_find_books_by_partial_author_ignoring_case():
    library = make_library()
    library.add_book(Book("9780135957059", "The Pragmatic Programmer", "David Thomas"))

    found = library.search_by_author("THOMAS")

    assert [book.isbn for book in found] == ["9780135957059"]


def test_should_list_only_books_with_copies_available():
    library = make_library(copies=1)
    library.add_book(Book("9780135957059", "The Pragmatic Programmer", "David Thomas", copies=0))

    available = library.get_available_books()

    assert [book.isbn for book in available] == [ISBN]
