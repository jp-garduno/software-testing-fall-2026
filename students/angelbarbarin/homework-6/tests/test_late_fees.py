from datetime import date
from decimal import Decimal

from book import Book
from member import Member, MemberCategory

ISBN = "0306406152"


def test_loan_is_due_fourteen_days_after_borrowing(library):
    library.borrow_book("M001", ISBN)
    assert library.get_loan("M001", ISBN).due_date == date(2026, 10, 15)


def test_late_fee_is_zero_on_due_date(library, clock):
    library.borrow_book("M001", ISBN)
    clock.advance(14)
    assert library.calculate_late_fee("M001", ISBN) == Decimal("0")


def test_late_fee_is_one_dollar_per_overdue_day(library, clock):
    library.borrow_book("M001", ISBN)
    clock.advance(17)
    assert library.calculate_late_fee("M001", ISBN) == Decimal("3.00")


def test_late_fee_uses_member_category_rate(library, clock):
    faculty = Member("F001", "Dra. Ruiz", category=MemberCategory.FACULTY)
    library.register_member(faculty)
    library.borrow_book("F001", ISBN)
    clock.advance(18)
    assert library.calculate_late_fee("F001", ISBN) == Decimal("2.00")


def test_total_fees_add_every_overdue_loan_of_member(library, clock):
    library.add_book(Book("9780132350884", "The Clean Coder", "Robert C. Martin"))
    library.borrow_book("M001", ISBN)
    library.borrow_book("M001", "9780132350884")
    clock.advance(16)
    assert library.total_fees_for_member("M001") == Decimal("4.00")


def test_total_fees_include_books_returned_late(library, clock):
    library.borrow_book("M001", ISBN)
    clock.advance(20)
    library.return_book("M001", ISBN)
    assert library.total_fees_for_member("M001") == Decimal("6.00")
