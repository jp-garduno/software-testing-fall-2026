from datetime import date

import pytest

from src.book import Book
from src.library import Library
from src.member import Member


@pytest.fixture
def library():
    lib = Library()
    lib.add_book(Book("1234567890", "Clean Code", "Robert Martin", copies=3))
    lib.add_book(Book("0987654321", "Refactoring", "Martin Fowler", copies=3))
    lib.register_member(Member("M001", "Alice"))
    lib.register_member(Member("M002", "Bob"))
    return lib


def test_borrow_is_recorded_in_member_history(library):
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    event = library.get_history("M001")[0]
    assert (event.action, event.isbn, event.date) == ("borrow", "1234567890", date(2026, 1, 1))


def test_return_is_recorded_in_member_history(library):
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    library.return_book("M001", "1234567890", return_date=date(2026, 1, 5))
    assert [e.action for e in library.get_history("M001")] == ["borrow", "return"]


def test_history_only_contains_events_of_that_member(library):
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    library.borrow_book("M002", "0987654321", borrow_date=date(2026, 1, 2))
    assert [e.isbn for e in library.get_history("M002")] == ["0987654321"]


def test_member_history_report_summarizes_activity(library):
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    library.borrow_book("M001", "0987654321", borrow_date=date(2026, 1, 2))
    library.return_book("M001", "1234567890", return_date=date(2026, 1, 5))
    assert library.member_history_report("M001") == {
        "member_id": "M001",
        "name": "Alice",
        "total_borrows": 2,
        "total_returns": 1,
        "currently_borrowed": ["0987654321"],
    }


def test_most_borrowed_book_is_the_isbn_borrowed_most_often(library):
    library.borrow_book("M001", "1234567890", borrow_date=date(2026, 1, 1))
    library.borrow_book("M002", "1234567890", borrow_date=date(2026, 1, 2))
    library.borrow_book("M001", "0987654321", borrow_date=date(2026, 1, 3))
    assert library.most_borrowed_book() == "1234567890"


def test_most_borrowed_book_is_none_without_borrows(library):
    assert library.most_borrowed_book() is None


def test_history_report_for_unknown_member_is_rejected(library):
    with pytest.raises(ValueError, match="Unknown member"):
        library.member_history_report("NOPE")
