from datetime import date
import pytest
from src.book import Book
from src.member import Member
from src.library import Library


def test_member_borrowing_history_tracking():
    lib = Library()
    b1 = Book("1111111111", "Clean Code", "Robert Martin", total_copies=2)
    b2 = Book("2222222222", "Refactoring", "Martin Fowler", total_copies=2)
    m1 = Member("M001", "Alice")
    lib.add_book(b1)
    lib.add_book(b2)
    lib.register_member(m1)

    lib.borrow_book("M001", "1111111111", borrow_date=date(2026, 10, 1))
    lib.return_book("M001", "1111111111", return_date=date(2026, 10, 10))
    lib.borrow_book("M001", "2222222222", borrow_date=date(2026, 10, 15))

    history = lib.get_member_history("M001")
    assert len(history) == 2
    assert history[0]["isbn"] == "1111111111"
    assert history[0]["status"] == "RETURNED"
    assert history[0]["return_date"] == date(2026, 10, 10)
    assert history[1]["isbn"] == "2222222222"
    assert history[1]["status"] == "ACTIVE"
    assert history[1]["return_date"] is None


def test_library_statistics():
    lib = Library()
    b1 = Book("1111111111", "Clean Code", "Robert Martin", total_copies=3)
    b2 = Book("2222222222", "Refactoring", "Martin Fowler", total_copies=2)
    m1 = Member("M001", "Alice", max_borrow_limit=5)
    m2 = Member("M002", "Bob", max_borrow_limit=5)
    lib.add_book(b1)
    lib.add_book(b2)
    lib.register_member(m1)
    lib.register_member(m2)

    # b1 borrowed twice, b2 borrowed once
    lib.borrow_book("M001", "1111111111", borrow_date=date(2026, 10, 1))
    lib.return_book("M001", "1111111111", return_date=date(2026, 10, 10))

    lib.borrow_book("M002", "1111111111", borrow_date=date(2026, 10, 12))
    lib.borrow_book("M001", "2222222222", borrow_date=date(2026, 10, 15))

    stats = lib.get_library_statistics()
    assert stats["total_borrows"] == 3
    assert stats["active_loans"] == 2
    assert stats["most_borrowed_isbn"] == "1111111111"
    assert stats["most_borrowed_count"] == 2


def test_member_history_raises_for_unregistered_member():
    lib = Library()
    with pytest.raises(KeyError, match="Member not registered"):
        lib.get_member_history("UNKNOWN")


def test_library_statistics_with_no_activity():
    lib = Library()
    stats = lib.get_library_statistics()
    assert stats["total_borrows"] == 0
    assert stats["active_loans"] == 0
    assert stats["most_borrowed_isbn"] is None
    assert stats["most_borrowed_count"] == 0
