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


def test_library_searches_books_by_title():
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

    results = library.search_by_title("Hobbit")

    assert len(results) == 1
    assert results[0] is book1


def test_library_searches_books_by_author():
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

    results = library.search_by_author("Tolkien")

    assert len(results) == 1
    assert results[0] is book1


def test_library_gets_only_available_books():
    library = Library()

    available_book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=2,
    )
    unavailable_book = Book(
        isbn="1234567891",
        title="Dune",
        author="Frank Herbert",
        total_copies=2,
        available_copies=0,
    )

    library.add_book(available_book)
    library.add_book(unavailable_book)

    results = library.get_available_books()

    assert len(results) == 1
    assert results[0] is available_book


def test_library_borrows_book_to_member():
    library = Library()

    book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )
    member = Member(
        member_id="M001",
        name="Katherine",
    )

    library.add_book(book)
    library.register_member(member)

    library.borrow_book("M001", "1234567890")

    assert book.available_copies == 2
    assert "1234567890" in member.borrowed_books


def test_library_cannot_borrow_unavailable_book():
    library = Library()

    book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=1,
        available_copies=0,
    )
    member = Member(
        member_id="M001",
        name="Katherine",
    )

    library.add_book(book)
    library.register_member(member)

    with pytest.raises(ValueError, match="No copies available"):
        library.borrow_book("M001", "1234567890")

    assert book.available_copies == 0
    assert not member.borrowed_books


def test_library_cannot_exceed_member_borrow_limit():
    library = Library()

    book1 = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=2,
        available_copies=2,
    )
    book2 = Book(
        isbn="1234567891",
        title="Dune",
        author="Frank Herbert",
        total_copies=2,
        available_copies=2,
    )
    member = Member(
        member_id="M001",
        name="Katherine",
        max_borrow_limit=1,
    )

    library.add_book(book1)
    library.add_book(book2)
    library.register_member(member)

    library.borrow_book("M001", "1234567890")

    with pytest.raises(ValueError, match="borrowing limit"):
        library.borrow_book("M001", "1234567891")

    assert book1.available_copies == 1
    assert book2.available_copies == 2
    assert member.borrowed_books == ["1234567890"]


def test_library_returns_book_from_member():
    library = Library()

    book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )
    member = Member(
        member_id="M001",
        name="Katherine",
    )

    library.add_book(book)
    library.register_member(member)

    library.borrow_book("M001", "1234567890")
    library.return_book("M001", "1234567890")

    assert book.available_copies == 3
    assert "1234567890" not in member.borrowed_books


def test_library_cannot_return_book_not_borrowed():
    library = Library()

    book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )
    member = Member(
        member_id="M001",
        name="Katherine",
    )

    library.add_book(book)
    library.register_member(member)

    with pytest.raises(ValueError, match="not borrowed"):
        library.return_book("M001", "1234567890")

    assert book.available_copies == 3
    assert not member.borrowed_books


def test_library_cannot_borrow_book_for_unregistered_member():
    library = Library()

    book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )

    library.add_book(book)

    with pytest.raises(ValueError, match="Member not found"):
        library.borrow_book("M999", "1234567890")

    assert book.available_copies == 3


def test_library_cannot_borrow_nonexistent_book():
    library = Library()
    member = Member(
        member_id="M001",
        name="Katherine",
    )

    library.register_member(member)

    with pytest.raises(ValueError, match="Book not found"):
        library.borrow_book("M001", "1234567890")

    assert not member.borrowed_books


def test_library_cannot_return_book_for_unregistered_member():
    library = Library()

    book = Book(
        isbn="1234567890",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        total_copies=3,
        available_copies=3,
    )
    library.add_book(book)

    with pytest.raises(ValueError, match="Member not found"):
        library.return_book("M999", "1234567890")

    assert book.available_copies == 3


def test_library_cannot_return_nonexistent_book():
    library = Library()

    member = Member(member_id="M001", name="Katherine")
    library.register_member(member)

    with pytest.raises(ValueError, match="Book not found"):
        library.return_book("M001", "1234567890")

    assert not member.borrowed_books


