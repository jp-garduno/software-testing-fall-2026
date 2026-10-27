"""Tests for the Library class."""

import pytest

from src.book import Book
from src.exceptions import BookNotFoundError, MemberNotFoundError
from src.library import Library
from src.member import Member


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
