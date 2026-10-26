"""Integration tests for catalog and borrowing operations."""

from datetime import date

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


def test_unknown_book_cannot_be_borrowed(stocked_library):
    with pytest.raises(KeyError):
        stocked_library.borrow_book("m1", "0000000000")


def test_return_book_restores_both_member_and_inventory(stocked_library):
    stocked_library.borrow_book("m1", "1234567890")
    stocked_library.return_book("m1", "1234567890")
    assert (stocked_library.members["m1"].borrowed_books,
            stocked_library.catalog["1234567890"].available_copies) == ([], 1)


def test_wrong_member_return_leaves_inventory_unchanged(stocked_library):
    stocked_library.borrow_book("m1", "1234567890")
    stocked_library.register_member(Member("m2", "Ana"))
    with pytest.raises(ValueError):
        stocked_library.return_book("m2", "1234567890")
    assert stocked_library.catalog["1234567890"].available_copies == 0


def test_search_by_title_matches_a_case_insensitive_substring(stocked_library):
    assert stocked_library.search_by_title("UN") == [
        stocked_library.catalog["1234567890"]
    ]


def test_search_by_author_matches_a_case_insensitive_substring(stocked_library):
    assert stocked_library.search_by_author("HERB") == [
        stocked_library.catalog["1234567890"]
    ]


def test_get_available_books_excludes_borrowed_out_titles(stocked_library):
    stocked_library.add_book(Book("1234567891", "Foundation", "Isaac Asimov"))
    stocked_library.borrow_book("m1", "1234567890")
    assert stocked_library.get_available_books() == [
        stocked_library.catalog["1234567891"]
    ]


def test_search_returns_an_empty_list_when_no_title_matches(stocked_library):
    assert stocked_library.search_by_title("missing") == []


def test_library_records_the_due_date_of_a_new_loan():
    library = Library(today=lambda: date(2026, 10, 1))
    library.add_book(Book("1234567890", "Dune", "Frank Herbert"))
    library.register_member(Member("m1", "Luis"))
    library.borrow_book("m1", "1234567890")
    assert library.get_due_date("m1", "1234567890") == date(2026, 10, 15)


def test_get_due_date_rejects_a_book_not_borrowed(stocked_library):
    with pytest.raises(ValueError, match="active"):
        stocked_library.get_due_date("m1", "1234567890")


@pytest.fixture
def dated_library():
    clock = [date(2026, 10, 1)]
    library = Library(today=lambda: clock[0])
    library.add_book(Book("1234567890", "Dune", "Frank Herbert"))
    library.register_member(Member("m1", "Luis"))
    return library, clock


def test_library_totals_a_members_overdue_fees(dated_library):
    library, clock = dated_library
    library.borrow_book("m1", "1234567890")
    clock[0] = date(2026, 10, 18)
    assert library.calculate_late_fees("m1") == 3


def test_library_return_stops_fee_growth(dated_library):
    library, clock = dated_library
    library.borrow_book("m1", "1234567890")
    clock[0] = date(2026, 10, 16)
    library.return_book("m1", "1234567890")
    clock[0] = date(2026, 10, 20)
    assert library.calculate_late_fees("m1") == 1


def test_library_does_not_charge_another_members_fees(dated_library):
    library, clock = dated_library
    library.register_member(Member("m2", "Ana"))
    library.borrow_book("m1", "1234567890")
    clock[0] = date(2026, 10, 20)
    assert library.calculate_late_fees("m2") == 0


def test_library_sums_fees_from_multiple_books(dated_library):
    library, clock = dated_library
    library.add_book(Book("1234567891", "Foundation", "Isaac Asimov"))
    library.borrow_book("m1", "1234567890")
    library.borrow_book("m1", "1234567891")
    clock[0] = date(2026, 10, 18)
    assert library.calculate_late_fees("m1") == 6


def test_returned_book_no_longer_has_an_active_due_date(stocked_library):
    stocked_library.borrow_book("m1", "1234567890")
    stocked_library.return_book("m1", "1234567890")
    with pytest.raises(ValueError, match="active"):
        stocked_library.get_due_date("m1", "1234567890")


def test_genre_filter_matches_without_case_sensitivity(stocked_library):
    book = Book("1234567891", "Foundation", "Isaac Asimov", genre="Science Fiction")
    stocked_library.add_book(book)
    assert stocked_library.search_with_filters(genre="science fiction") == [book]


def test_publication_year_filter_excludes_missing_metadata(stocked_library):
    book = Book("1234567891", "Foundation", "Isaac Asimov", publication_year=1951)
    stocked_library.add_book(book)
    assert stocked_library.search_with_filters(publication_year=1951) == [book]
