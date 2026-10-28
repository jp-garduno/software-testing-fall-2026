from book import Book
from library import Library
from member import Member
from datetime import date, timedelta

import pytest


def test_library_adds_books_and_registers_members():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    member = Member("m-1", "Ada")

    library.add_book(book)
    library.register_member(member)

    assert library.books[book.isbn] is book


def test_library_rejects_duplicate_books_and_members():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    member = Member("m-1", "Ada")
    library.add_book(book)
    library.register_member(member)

    with pytest.raises(ValueError, match="ISBN"):
        library.add_book(book)
    with pytest.raises(ValueError, match="ID"):
        library.register_member(member)


def configured_library():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin", 2)
    member = Member("m-1", "Ada")
    library.add_book(book)
    library.register_member(member)
    return library, book, member


def test_library_borrows_book_for_member():
    library, book, member = configured_library()

    library.borrow_book(member.member_id, book.isbn)

    assert book.isbn in member.borrowed_books


def test_library_returns_book_for_member():
    library, book, member = configured_library()
    library.borrow_book(member.member_id, book.isbn)

    library.return_book(member.member_id, book.isbn)

    assert book.available_copies == 2


def test_library_rejects_unknown_book_or_member():
    library = Library()

    with pytest.raises(ValueError, match="member"):
        library.borrow_book("missing", "1234567890")
    library.register_member(Member("m-1", "Ada"))
    with pytest.raises(ValueError, match="book"):
        library.borrow_book("m-1", "1234567890")


def test_library_searches_title_author_and_availability():
    library, book, _ = configured_library()

    assert library.search_by_title("clean") == [book]
    assert library.search_by_author("martin") == [book]
    assert library.get_available_books() == [book]


def test_library_calculates_one_dollar_per_overdue_day():
    library, book, member = configured_library()
    library.borrow_book(member.member_id, book.isbn)
    library.borrowing_history[-1]["due_date"] = date.today() - timedelta(days=3)

    assert library.calculate_late_fees(member.member_id) == 3


def test_library_rejects_fees_for_an_unknown_member():
    with pytest.raises(ValueError, match="member"):
        Library().calculate_late_fees("missing")


def test_library_restores_inventory_when_member_limit_is_reached():
    library, book, member = configured_library()
    member.max_borrow_limit = 1
    library.borrow_book(member.member_id, book.isbn)

    with pytest.raises(ValueError, match="limit"):
        library.borrow_book(member.member_id, book.isbn)

    assert book.available_copies == 1


def test_library_reserves_unavailable_book_in_fifo_order():
    library, book, member = configured_library()
    second = Member("m-2", "Grace")
    library.register_member(second)
    library.borrow_book(member.member_id, book.isbn)
    library.borrow_book(second.member_id, book.isbn)

    library.reserve_book(member.member_id, book.isbn)
    library.reserve_book(second.member_id, book.isbn)

    assert library.reservations[book.isbn] == [member.member_id, second.member_id]
