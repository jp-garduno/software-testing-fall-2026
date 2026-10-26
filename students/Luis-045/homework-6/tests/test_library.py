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


def test_register_member_rejects_a_duplicate_id():
    library = Library()
    library.register_member(Member("m1", "Luis"))
    with pytest.raises(ValueError, match="already"):
        library.register_member(Member("m1", "Other"))


@pytest.fixture
def stocked_library():
    library = Library()
    library.add_book(Book("1234567890", "Dune", "Frank Herbert"))
    library.register_member(Member("m1", "Luis"))
    return library


def test_borrow_book_updates_member_and_inventory(stocked_library):
    stocked_library.borrow_book("m1", "1234567890")
    assert (stocked_library.members["m1"].borrowed_books,
            stocked_library.catalog["1234567890"].available_copies) == (
                ["1234567890"], 0
            )


def test_unavailable_book_does_not_change_member_loans(stocked_library):
    stocked_library.borrow_book("m1", "1234567890")
    stocked_library.register_member(Member("m2", "Ana"))
    with pytest.raises(ValueError, match="available"):
        stocked_library.borrow_book("m2", "1234567890")
    assert stocked_library.members["m2"].borrowed_books == []


def test_limit_failure_leaves_inventory_unchanged(stocked_library):
    stocked_library.members["m1"].max_borrow_limit = 0
    with pytest.raises(ValueError, match="limit"):
        stocked_library.borrow_book("m1", "1234567890")
    assert stocked_library.catalog["1234567890"].available_copies == 1


def test_unknown_member_cannot_borrow(stocked_library):
    with pytest.raises(KeyError):
        stocked_library.borrow_book("missing", "1234567890")
