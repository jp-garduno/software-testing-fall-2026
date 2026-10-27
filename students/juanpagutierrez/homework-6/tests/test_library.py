"""Tests for the Library class."""

import pytest

from src.book import Book
from src.exceptions import BookNotFoundError, BookUnavailableError, BorrowLimitExceededError, MemberNotFoundError
from src.library import Library
from src.member import Member

ISBN = "1234567890"
MEMBER_ID = "M001"


@pytest.fixture(name="library")
def library_fixture():
    """A library with one single-copy book and one registered member."""
    library = Library()
    library.add_book(Book(ISBN, "Clean Code", "Robert Martin"))
    library.register_member(Member(MEMBER_ID, "Ada Lovelace"))
    return library


def test_added_book_can_be_found_by_isbn():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    library.add_book(book)
    assert library.get_book("1234567890") is book


def test_get_book_with_unknown_isbn_raises():
    with pytest.raises(BookNotFoundError):
        Library().get_book("1234567890")


def test_adding_a_book_with_existing_isbn_raises():
    library = Library()
    library.add_book(Book("1234567890", "Clean Code", "Robert Martin"))
    with pytest.raises(ValueError):
        library.add_book(Book("1234567890", "Other", "Someone"))


def test_registered_member_can_be_found_by_id():
    library = Library()
    member = Member("M001", "Ada Lovelace")
    library.register_member(member)
    assert library.get_member("M001") is member


def test_get_member_with_unknown_id_raises():
    with pytest.raises(MemberNotFoundError):
        Library().get_member("M999")


def test_registering_a_duplicate_member_id_raises():
    library = Library()
    library.register_member(Member("M001", "Ada Lovelace"))
    with pytest.raises(ValueError):
        library.register_member(Member("M001", "Grace Hopper"))


def test_borrow_book_takes_a_copy_off_the_shelf(library):
    library.borrow_book(MEMBER_ID, ISBN)
    assert library.get_book(ISBN).available_copies == 0


def test_borrow_book_records_the_loan_on_the_member(library):
    library.borrow_book(MEMBER_ID, ISBN)
    assert library.get_member(MEMBER_ID).borrowed_books == [ISBN]


def test_failed_borrow_over_limit_keeps_the_copy_on_the_shelf(library):
    library.add_book(Book("0987654321", "Refactoring", "Martin Fowler", total_copies=2))
    library.register_member(Member("M002", "Grace Hopper", max_borrow_limit=0))
    with pytest.raises(BorrowLimitExceededError):
        library.borrow_book("M002", "0987654321")
    assert library.get_book("0987654321").available_copies == 2


def test_failed_borrow_of_unavailable_book_leaves_member_unchanged(library):
    library.register_member(Member("M002", "Grace Hopper"))
    library.borrow_book(MEMBER_ID, ISBN)
    with pytest.raises(BookUnavailableError):
        library.borrow_book("M002", ISBN)
    assert library.get_member("M002").borrowed_books == []
