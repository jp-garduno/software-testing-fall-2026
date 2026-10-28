"""Behavior specifications for the library management domain."""

import pytest

from src.library import Library

from src.book import Book
from src.member import Member


def test_library_starts_with_empty_catalog_and_members():
    catalog = Library()
    assert (catalog.catalog, catalog.members) == ({}, {})


def test_library_adds_book_by_isbn():
    catalog = Library()
    book = Book("1234567890", "Pedro Paramo", "Juan Rulfo")
    catalog.add_book(book)
    assert catalog.catalog[book.isbn] is book


def test_duplicate_isbn_does_not_replace_catalog_entry():
    catalog = Library()
    original = Book("1234567890", "Original", "Author")
    catalog.add_book(original)
    with pytest.raises(ValueError, match="registered"):
        catalog.add_book(Book(original.isbn, "Replacement", "Author"))
    assert catalog.catalog[original.isbn] is original


def test_register_member_indexes_identity():
    catalog = Library()
    member = Member("M1", "Ana")
    catalog.register_member(member)
    assert catalog.members["M1"] is member


def test_duplicate_member_does_not_replace_existing_member(library):
    original = library.members["M1"]
    with pytest.raises(ValueError, match="registered"):
        library.register_member(Member("M1", "Other"))
    assert library.members["M1"] is original


def test_borrow_updates_stock_and_member_together(library):
    library.borrow_book("M1", "1234567890")
    assert (
        library.catalog["1234567890"].available_copies,
        library.members["M1"].borrowed_books,
    ) == (1, ["1234567890"])


def test_unknown_borrower_does_not_change_stock(library):
    with pytest.raises(ValueError, match="Unknown member"):
        library.borrow_book("missing", "1234567890")
    assert library.catalog["1234567890"].available_copies == 2


def test_unknown_book_does_not_change_member(library):
    with pytest.raises(ValueError, match="Unknown book"):
        library.borrow_book("M1", "9999999999")
    assert library.members["M1"].borrowed_books == []


def test_failed_borrow_at_limit_is_atomic(library):
    library.register_member(Member("M2", "Luis", max_borrow_limit=1))
    library.add_book(Book("9999999999", "Other", "Author"))
    library.borrow_book("M2", "9999999999")
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("M2", "1234567890")
    assert library.catalog["1234567890"].available_copies == 2


def test_failed_duplicate_borrow_is_atomic(library):
    library.borrow_book("M1", "1234567890")
    with pytest.raises(ValueError, match="already"):
        library.borrow_book("M1", "1234567890")
    assert library.catalog["1234567890"].available_copies == 1


def test_library_return_restores_stock_and_capacity(library):
    library.borrow_book("M1", "1234567890")
    library.return_book("M1", "1234567890")
    assert (
        library.catalog["1234567890"].available_copies,
        library.members["M1"].borrowed_books,
    ) == (2, [])


def test_return_rejects_unknown_member(library):
    with pytest.raises(ValueError, match="Unknown member"):
        library.return_book("missing", "1234567890")


def test_return_rejects_unknown_book(library):
    with pytest.raises(ValueError, match="Unknown book"):
        library.return_book("M1", "9999999999")


def test_search_title_matches_substrings_case_insensitively(library):
    assert [book.isbn for book in library.search_by_title("  PEDRO  ")] == [
        "1234567890"
    ]


def test_search_author_returns_all_matching_books(library):
    assert len(library.search_by_author("RULFO")) == 2


def test_available_books_excludes_out_of_stock_titles(library):
    assert [book.isbn for book in library.get_available_books()] == ["1234567890"]


def test_unavailable_loan_does_not_record_member_borrow(library):
    with pytest.raises(ValueError, match="available"):
        library.borrow_book("M1", "1234567890123")
    assert library.members["M1"].borrowed_books == []


def test_return_by_nonborrower_preserves_inventory(library):
    library.borrow_book("M1", "1234567890")
    library.register_member(Member("M2", "Luis"))
    with pytest.raises(ValueError, match="not borrowed"):
        library.return_book("M2", "1234567890")
    assert library.catalog["1234567890"].available_copies == 1


@pytest.mark.parametrize("method", ["search_by_title", "search_by_author"])
def test_search_returns_empty_for_no_matches(library, method):
    assert getattr(library, method)("missing") == []


def test_blank_title_query_returns_entire_catalog(library):
    assert len(library.search_by_title("  ")) == 2
