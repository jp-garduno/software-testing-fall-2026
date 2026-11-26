"""Tests for the Library class."""
# pylint: disable=missing-function-docstring

import pytest

from src.book import Book
from src.errors import LibraryError
from src.library import Library
from src.member import Member

from tests.helpers import ISBN, make_library


def test_added_book_can_be_found_by_isbn():
    library = Library()
    book = Book(ISBN, "Clean Code", "Robert Martin")
    library.add_book(book)
    assert library.find_book(ISBN) is book


def test_adding_same_isbn_twice_raises_error():
    library = Library()
    library.add_book(Book(ISBN, "Clean Code", "Robert Martin"))
    with pytest.raises(LibraryError):
        library.add_book(Book(ISBN, "Other", "Someone"))


def test_registered_member_can_be_found_by_id():
    library = Library()
    member = Member("m1", "Ana")
    library.register_member(member)
    assert library.find_member("m1") is member


def test_registering_same_member_twice_raises_error():
    library = Library()
    library.register_member(Member("m1", "Ana"))
    with pytest.raises(LibraryError):
        library.register_member(Member("m1", "Bo"))


def test_borrow_book_takes_a_copy_from_the_catalog():
    library = make_library()
    library.borrow_book("m1", ISBN)
    assert library.find_book(ISBN).available_copies == 0


def test_borrow_book_records_the_loan_on_the_member():
    library = make_library()
    library.borrow_book("m1", ISBN)
    assert library.find_member("m1").borrowed_books == [ISBN]


def test_borrow_with_unknown_member_raises_error():
    library = make_library()
    with pytest.raises(LibraryError):
        library.borrow_book("nobody", ISBN)


def test_borrow_with_unknown_book_raises_error():
    library = make_library()
    with pytest.raises(LibraryError):
        library.borrow_book("m1", "0000000000")


def test_borrow_over_limit_does_not_consume_a_copy():
    library = make_library()
    library.register_member(Member("m2", "Bo", max_borrow_limit=0))
    with pytest.raises(LibraryError):
        library.borrow_book("m2", ISBN)
    assert library.find_book(ISBN).available_copies == 1


def test_return_book_gives_the_copy_back():
    library = make_library()
    library.borrow_book("m1", ISBN)
    library.return_book("m1", ISBN)
    assert library.find_book(ISBN).available_copies == 1


def test_return_book_clears_the_loan_on_the_member():
    library = make_library()
    library.borrow_book("m1", ISBN)
    library.return_book("m1", ISBN)
    assert library.find_member("m1").borrowed_books == []


def test_return_with_unknown_member_raises_error():
    library = make_library()
    with pytest.raises(LibraryError):
        library.return_book("nobody", ISBN)


def test_return_of_book_not_borrowed_raises_error():
    library = make_library()
    with pytest.raises(LibraryError):
        library.return_book("m1", ISBN)


def test_search_by_title_matches_part_of_title_ignoring_case():
    library = make_library()
    assert library.search_by_title("clean") == [library.find_book(ISBN)]


def test_search_by_title_returns_empty_list_without_matches():
    library = make_library()
    assert library.search_by_title("python") == []


def test_search_by_author_matches_part_of_author_ignoring_case():
    library = make_library()
    assert library.search_by_author("MARTIN") == [library.find_book(ISBN)]


def test_search_by_author_returns_empty_list_without_matches():
    library = make_library()
    assert library.search_by_author("fowler") == []


def test_get_available_books_skips_books_without_copies():
    library = make_library()
    library.add_book(Book("0987654321", "Refactoring", "Fowler", copies=0))
    assert library.get_available_books() == [library.find_book(ISBN)]
