"""Tests for the Library class."""

import pytest

from src.book import Book
from src.exceptions import BookNotFoundError, MemberNotFoundError
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
