from datetime import date
import pytest
from src.book import Book
from src.library import Library
from src.member import Member


def test_loan_due_date(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    loan = library.loans[0]
    assert (loan["member_id"], loan["isbn"], loan["borrowed_on"], loan["due_on"]) == (
        "m1", "1234567890", date(2026, 10, 1), date(2026, 10, 15))


def test_total_overdue_fees(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 2))
    assert library.calculate_late_fees("m1", as_of=date(2026, 10, 18)) == 5


def test_record_return_date(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 17))
    assert library.loans[0]["returned_on"] == date(2026, 10, 17)


def test_returned_fees_stop_growing(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 17))
    assert library.calculate_late_fees("m1", as_of=date(2026, 11, 1)) == 2


def test_return_before_borrow_is_atomic(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 10))
    with pytest.raises(ValueError, match="before"):
        library.return_book("m1", "1234567890", returned_on=date(2026, 10, 9))
    assert (library.catalog["1234567890"].available_copies,
            library.members["m1"].borrowed_books) == (1, ["1234567890"])


def test_unknown_member_fees(library):
    with pytest.raises(ValueError, match="member"):
        library.calculate_late_fees("missing", as_of=date(2026, 10, 20))


def test_member_history_report(library):
    library.register_member(Member("m2", "Luis"))
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.borrow_book("m2", "1234567890", borrowed_on=date(2026, 10, 2))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 17))
    report = library.member_history("m1")
    assert [(loan["isbn"], loan["returned_on"]) for loan in report] == [
        ("1234567890", date(2026, 10, 17))]


def test_active_history_has_no_return_date(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    assert library.member_history("m1")[0]["returned_on"] is None


def test_most_borrowed_book(library):
    library.add_book(Book("1234567890123", "Foundation", "Isaac Asimov"))
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 2))
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 3))
    library.borrow_book("m1", "1234567890123", borrowed_on=date(2026, 10, 4))
    assert library.most_borrowed_book().isbn == "1234567890"


def test_most_borrowed_without_loans(library):
    assert library.most_borrowed_book() is None
