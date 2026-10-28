import pytest

from src.book import Book
from src.exceptions import (
    BookNotFoundError,
    DuplicateBookError,
    DuplicateMemberError,
    MemberNotFoundError,
)
from src.library import Library
from src.member import Member


def test_added_book_can_be_found_by_isbn():
    library = Library()
    book = Book("1234567890", "Test Book", "Author")
    library.add_book(book)
    assert library.get_book("1234567890") is book


def test_adding_a_duplicate_isbn_raises():
    library = Library()
    library.add_book(Book("1234567890", "Test Book", "Author"))
    with pytest.raises(DuplicateBookError):
        library.add_book(Book("1234567890", "Other", "Author"))


def test_get_book_raises_for_unknown_isbn():
    with pytest.raises(BookNotFoundError):
        Library().get_book("0000000000")


def test_registered_member_can_be_found_by_id():
    library = Library()
    member = Member("M1", "Ana")
    library.register_member(member)
    assert library.get_member("M1") is member


def test_registering_a_duplicate_member_id_raises():
    library = Library()
    library.register_member(Member("M1", "Ana"))
    with pytest.raises(DuplicateMemberError):
        library.register_member(Member("M1", "Otra Ana"))


def test_get_member_raises_for_unknown_id():
    with pytest.raises(MemberNotFoundError):
        Library().get_member("X")
