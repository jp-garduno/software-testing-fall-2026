"""Integration tests for catalog and borrowing operations."""

import pytest

from src.book import Book
from src.library import Library
from src.member import Member


def test_library_starts_with_empty_catalog_and_members():
    library = Library()
    assert (library.catalog, library.members) == ({}, {})


def test_add_book_indexes_the_book_by_isbn():
    library = Library()
    book = Book("1234567890", "Dune", "Frank Herbert")
    library.add_book(book)
    assert library.catalog[book.isbn] is book


def test_register_member_indexes_the_member_by_id():
    library = Library()
    member = Member("m1", "Luis")
    library.register_member(member)
    assert library.members[member.member_id] is member


def test_add_book_rejects_a_duplicate_isbn():
    library = Library()
    library.add_book(Book("1234567890", "Dune", "Frank Herbert"))
    with pytest.raises(ValueError, match="already"):
        library.add_book(Book("1234567890", "Replacement", "Other"))
