"""Unit tests for the Library class and advanced features developed with TDD."""

from datetime import date, timedelta

import pytest
from src.book import Book
from src.library import Library
from src.member import Member


def test_library_adds_book_to_catalog():
    library = Library()
    book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )

    library.add_book(book)

    assert "1234567890" in library.books
    assert library.books["1234567890"] is book


def test_library_can_add_multiple_books():
    library = Library()

    book1 = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )
    book2 = Book(
        isbn="1234567891",
        title="Dune",
        author="Frank Herbert",
        total_copies=2,
        available_copies=2,
    )

    library.add_book(book1)
    library.add_book(book2)

    assert len(library.books) == 2
    assert library.books["1234567890"] is book1
    assert library.books["1234567891"] is book2


def test_library_rejects_duplicate_isbn():
    library = Library()

    book1 = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )
    book2 = Book(
        isbn="1234567890",
        title="Different Book",
        author="Another Author",
        total_copies=2,
        available_copies=2,
    )

    library.add_book(book1)

    with pytest.raises(ValueError, match="already exists"):
        library.add_book(book2)


def test_library_registers_member():
    library = Library()
    member = Member(
        member_id="M001",
        name="Katherine",
    )

    library.register_member(member)

    assert "M001" in library.members
    assert library.members["M001"] is member


def test_library_rejects_duplicate_member_id():
    library = Library()

    member1 = Member(
        member_id="M001",
        name="Katherine",
    )
    member2 = Member(
        member_id="M001",
        name="Another Member",
    )

    library.register_member(member1)

    with pytest.raises(ValueError, match="already exists"):
        library.register_member(member2)


