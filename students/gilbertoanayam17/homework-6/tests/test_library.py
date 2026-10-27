"""Tests for Library: catalog, members, borrowing, returning and searching."""

import pytest

from src import errors
from src.book import Book
from src.library import Library
from src.member import Member

ISBN = "1234567890"


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
