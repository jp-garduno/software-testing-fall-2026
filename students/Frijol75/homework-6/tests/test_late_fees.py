from datetime import date, timedelta
import pytest
from src.book import Book
from src.member import Member
from src.library import Library
from src.loan import LoanRecord, calculate_late_fee


def test_loan_record_creation_with_default_14_day_due_date():
    borrow_date = date(2026, 10, 1)
    loan = LoanRecord(
        loan_id="L001",
        member_id="M001",
        isbn="1234567890",
        borrow_date=borrow_date,
    )
    assert loan.loan_id == "L001"
    assert loan.member_id == "M001"
    assert loan.isbn == "1234567890"
    assert loan.borrow_date == borrow_date
    assert loan.due_date == date(2026, 10, 15)
    assert loan.return_date is None


def test_calculate_late_fee_on_time_return():
    borrow_date = date(2026, 10, 1)
    loan = LoanRecord("L001", "M001", "1234567890", borrow_date=borrow_date)
    return_date = date(2026, 10, 15)  # On due date
    fee = calculate_late_fee(loan, return_date=return_date, daily_rate=1.0)
    assert fee == 0.0


def test_calculate_late_fee_overdue_return():
    borrow_date = date(2026, 10, 1)
    loan = LoanRecord("L001", "M001", "1234567890", borrow_date=borrow_date)
    return_date = date(2026, 10, 20)  # 5 days overdue
    fee = calculate_late_fee(loan, return_date=return_date, daily_rate=1.0)
    assert fee == 5.0


def test_library_calculates_total_member_late_fees():
    lib = Library()
    book = Book("1234567890", "Refactoring", "Martin Fowler")
    member = Member("M001", "Alice")
    lib.add_book(book)
    lib.register_member(member)

    borrow_date = date(2026, 10, 1)
    lib.borrow_book("M001", "1234567890", borrow_date=borrow_date)

    as_of_date = date(2026, 10, 18)  # 3 days overdue
    total_fee = lib.calculate_member_late_fees("M001", as_of_date=as_of_date)
    assert total_fee == 3.0


def test_library_late_fees_for_multiple_books_and_returned_loans():
    lib = Library()
    book1 = Book("1111111111", "Book 1", "Author", total_copies=2)
    book2 = Book("2222222222", "Book 2", "Author", total_copies=2)
    member = Member("M001", "Alice", max_borrow_limit=5)
    lib.add_book(book1)
    lib.add_book(book2)
    lib.register_member(member)

    # Book 1: borrowed on Oct 1, returned on Oct 20 (5 days late = $5)
    lib.borrow_book("M001", "1111111111", borrow_date=date(2026, 10, 1))
    lib.return_book("M001", "1111111111", return_date=date(2026, 10, 20))

    # Book 2: borrowed on Oct 1, still unreturned on Oct 25 (10 days late = $10)
    lib.borrow_book("M001", "2222222222", borrow_date=date(2026, 10, 1))

    total = lib.calculate_member_late_fees("M001", as_of_date=date(2026, 10, 25))
    assert total == 15.0


def test_library_calculate_late_fees_raises_for_unregistered_member():
    lib = Library()
    with pytest.raises(KeyError, match="Member not registered"):
        lib.calculate_member_late_fees("NON_EXISTENT")
