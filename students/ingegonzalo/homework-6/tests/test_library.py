from datetime import date

import pytest

from src.book import Book
from src.history import HistoryEntry
from src.library import Library
from src.member import Member


@pytest.fixture
def library():
    return Library()


# --- catálogo ---
def test_new_library_has_no_available_books(library):
    assert library.get_available_books() == []


def test_add_book_makes_it_available_in_catalog(library):
    book = Book("1234567890", "Test Book", "Author")
    library.add_book(book)
    assert library.get_available_books() == [book]


def test_get_available_books_excludes_books_without_copies(library):
    available = Book("1111111111", "Available", "Author", total_copies=1)
    unavailable = Book("2222222222", "Unavailable", "Author", total_copies=0)
    library.add_book(available)
    library.add_book(unavailable)
    assert library.get_available_books() == [available]


def test_add_book_rejects_duplicate_isbn(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    with pytest.raises(ValueError):
        library.add_book(Book("1234567890", "Another Book", "Author"))


# --- miembros ---
def test_register_member_makes_member_retrievable(library):
    member = Member("M001", "Ana")
    library.register_member(member)
    assert library.get_member("M001") is member


def test_get_member_raises_error_when_not_registered(library):
    with pytest.raises(ValueError, match="not registered"):
        library.get_member("M999")


def test_register_member_rejects_duplicate_id(library):
    library.register_member(Member("M001", "Ana"))
    with pytest.raises(ValueError):
        library.register_member(Member("M001", "Beto"))


# --- préstamos ---
def test_borrow_book_decreases_available_copies(library):
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    library.add_book(book)
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890")
    assert book.available_copies == 1


def test_borrow_book_adds_isbn_to_member(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    member = Member("M001", "Ana")
    library.register_member(member)
    library.borrow_book("M001", "1234567890")
    assert "1234567890" in member.borrowed_books


def test_borrow_book_raises_error_when_book_not_in_catalog(library):
    library.register_member(Member("M001", "Ana"))
    with pytest.raises(ValueError, match="not in the catalog"):
        library.borrow_book("M001", "9999999999")


def test_borrow_book_does_not_consume_copy_when_member_at_limit(library):
    first = Book("1111111111", "First", "Author")
    second = Book("2222222222", "Second", "Author")
    library.add_book(first)
    library.add_book(second)
    library.register_member(Member("M001", "Ana", max_borrow_limit=1))
    library.borrow_book("M001", "1111111111")
    with pytest.raises(ValueError):
        library.borrow_book("M001", "2222222222")
    assert second.available_copies == 1


def test_borrow_book_does_not_register_loan_when_book_unavailable(library):
    library.add_book(Book("1234567890", "Test Book", "Author", total_copies=0))
    member = Member("M001", "Ana")
    library.register_member(member)
    with pytest.raises(ValueError):
        library.borrow_book("M001", "1234567890")
    assert member.borrowed_books == []


def test_return_book_increases_available_copies(library):
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    library.add_book(book)
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890")
    library.return_book("M001", "1234567890")
    assert book.available_copies == 2


def test_return_book_removes_isbn_from_member(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    member = Member("M001", "Ana")
    library.register_member(member)
    library.borrow_book("M001", "1234567890")
    library.return_book("M001", "1234567890")
    assert member.borrowed_books == []


def test_return_book_does_not_change_copies_when_member_did_not_borrow_it(library):
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    library.add_book(book)
    library.register_member(Member("M001", "Ana"))
    library.register_member(Member("M002", "Beto"))
    library.borrow_book("M001", "1234567890")
    with pytest.raises(ValueError):
        library.return_book("M002", "1234567890")
    assert book.available_copies == 1


# --- búsquedas ---
def test_search_by_title_finds_matching_book(library):
    book = Book("1234567890", "Clean Code", "Robert Martin")
    library.add_book(book)
    library.add_book(Book("0987654321", "Refactoring", "Martin Fowler"))
    assert library.search_by_title("Clean Code") == [book]


def test_search_by_title_is_partial_and_case_insensitive(library):
    book = Book("1234567890", "Learning Python", "Author")
    library.add_book(book)
    assert library.search_by_title("python") == [book]


def test_search_by_author_finds_matching_books(library):
    book = Book("1234567890", "Clean Code", "Robert Martin")
    library.add_book(book)
    library.add_book(Book("0987654321", "Refactoring", "Martin Fowler"))
    assert library.search_by_author("robert") == [book]


# --- multas ---
def test_return_book_on_time_charges_no_late_fee(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    fee = library.return_book("M001", "1234567890", return_date=date(2026, 1, 10))
    assert fee == 0


def test_return_book_overdue_returns_late_fee(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    fee = library.return_book("M001", "1234567890", return_date=date(2026, 1, 18))
    assert fee == 3


def test_overdue_return_adds_fee_to_member_total(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    member = Member("M001", "Ana")
    library.register_member(member)
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    library.return_book("M001", "1234567890", return_date=date(2026, 1, 18))
    assert member.late_fees == 3


def test_late_fee_uses_member_category_rate(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    library.register_member(Member("M001", "Visitante", category="public"))
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    fee = library.return_book("M001", "1234567890", return_date=date(2026, 1, 18))
    assert fee == 6


# --- historial ---
def test_borrow_is_recorded_in_history(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    assert library.get_history() == [
        HistoryEntry("M001", "1234567890", "borrow", date(2026, 1, 1))
    ]


def test_return_is_recorded_in_history(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    library.return_book("M001", "1234567890", return_date=date(2026, 1, 5))
    assert library.get_history()[-1] == HistoryEntry(
        "M001", "1234567890", "return", date(2026, 1, 5)
    )


def test_get_member_history_returns_only_that_members_entries(library):
    library.add_book(Book("1111111111", "First", "Author"))
    library.add_book(Book("2222222222", "Second", "Author"))
    library.register_member(Member("M001", "Ana"))
    library.register_member(Member("M002", "Beto"))
    library.borrow_book("M001", "1111111111", borrow_date=date(2026, 1, 1))
    library.borrow_book("M002", "2222222222", borrow_date=date(2026, 1, 2))
    assert library.get_member_history("M001") == [
        HistoryEntry("M001", "1111111111", "borrow", date(2026, 1, 1))
    ]


def test_get_member_history_raises_error_for_unknown_member(library):
    with pytest.raises(ValueError, match="not registered"):
        library.get_member_history("M999")


def test_member_report_lists_each_event(library):
    library.add_book(Book("1234567890", "Test Book", "Author"))
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    library.return_book("M001", "1234567890", return_date=date(2026, 1, 5))
    assert library.generate_member_report("M001") == (
        "History for Ana (M001)\n"
        "2026-01-01 BORROW Test Book (1234567890)\n"
        "2026-01-05 RETURN Test Book (1234567890)"
    )


def test_most_borrowed_book_returns_book_with_most_borrows(library):
    popular = Book("1111111111", "Popular", "Author", total_copies=2)
    rare = Book("2222222222", "Rare", "Author")
    library.add_book(popular)
    library.add_book(rare)
    library.register_member(Member("M001", "Ana"))
    library.register_member(Member("M002", "Beto"))
    library.borrow_book("M001", "1111111111")
    library.borrow_book("M002", "1111111111")
    library.borrow_book("M001", "2222222222")
    assert library.most_borrowed_book() is popular


def test_most_borrowed_book_is_none_when_nothing_borrowed(library):
    assert library.most_borrowed_book() is None

def test_return_book_raises_error_when_book_not_in_catalog(library):
    library.register_member(Member("M001", "Ana"))
    with pytest.raises(ValueError, match="not in the catalog"):
        library.return_book("M001", "9999999999")


def test_get_history_returns_a_copy(library):
    library.get_history().append("intruder")
    assert library.get_history() == []