"""Tests for the selected advanced library features."""

from datetime import date, timedelta

import pytest

from book import Book
from library import Library
from member import Member


def populated_library():
    """Create a library with an unavailable book and three members."""
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin", copies=1)
    first = Member("m-1", "Ada", category="student")
    second = Member("m-2", "Grace", category="faculty")
    third = Member("m-3", "Linus", category="public")
    library.add_book(book)
    for member in (first, second, third):
        library.register_member(member)
    library.borrow_book(first.member_id, book.isbn)
    return library, book, first, second, third


def test_late_fees_use_the_member_category_rate():
    library, book, first, second, _ = populated_library()
    library.return_book(first.member_id, book.isbn)
    library.borrow_book(second.member_id, book.isbn)
    library.borrowing_history[-1]["due_date"] = date.today() - timedelta(days=3)

    assert library.calculate_late_fees(second.member_id) == 1.5


def test_late_fees_ignore_returned_and_not_yet_due_loans():
    library, book, first, _, _ = populated_library()
    library.borrowing_history[-1]["due_date"] = date.today() - timedelta(days=8)
    library.return_book(first.member_id, book.isbn)

    assert library.calculate_late_fees(first.member_id) == 0


def test_reservation_queue_notifies_the_first_waiting_member_after_return():
    library, book, first, second, third = populated_library()
    library.reserve_book(second.member_id, book.isbn)
    library.reserve_book(third.member_id, book.isbn)

    notified_member = library.return_book(first.member_id, book.isbn)

    assert notified_member == second.member_id
    assert library.next_reservation(book.isbn) == third.member_id


def test_reservation_queue_returns_none_when_there_are_no_waiting_members():
    library, book, first, _, _ = populated_library()

    assert library.return_book(first.member_id, book.isbn) is None


def test_available_books_cannot_be_reserved():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    member = Member("m-1", "Ada")
    library.add_book(book)
    library.register_member(member)

    with pytest.raises(ValueError, match="available"):
        library.reserve_book(member.member_id, book.isbn)


def test_member_cannot_reserve_the_same_book_twice():
    library, book, _, second, _ = populated_library()
    library.reserve_book(second.member_id, book.isbn)

    with pytest.raises(ValueError, match="already"):
        library.reserve_book(second.member_id, book.isbn)


@pytest.mark.parametrize(
    ("category", "days_late", "expected_fee"),
    [("student", 2, 2.0), ("faculty", 2, 1.0), ("public", 2, 3.0)],
)
def test_each_category_has_its_documented_late_fee(category, days_late, expected_fee):
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    member = Member("m-1", "Ada", category=category)
    library.add_book(book)
    library.register_member(member)
    library.borrow_book(member.member_id, book.isbn)
    library.borrowing_history[-1]["due_date"] = date.today() - timedelta(days=days_late)

    assert library.calculate_late_fees(member.member_id) == expected_fee
