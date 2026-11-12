"""Advanced feature 1: late fees ($1/day for students, due 14 days after borrowing)."""

from datetime import timedelta

import pytest

from src.loan import Loan
from tests.conftest import CLEAN_CODE, REFACTORING, START_DATE


def test_loan_is_due_fourteen_days_after_borrowing():
    loan = Loan("S1", CLEAN_CODE, borrowed_on=START_DATE)
    assert loan.due_on == START_DATE + timedelta(days=14)


def test_loan_is_not_overdue_on_its_due_date():
    loan = Loan("S1", CLEAN_CODE, borrowed_on=START_DATE)
    assert loan.days_overdue(loan.due_on) == 0


def test_loan_is_one_day_overdue_the_day_after_due_date():
    loan = Loan("S1", CLEAN_CODE, borrowed_on=START_DATE)
    assert loan.days_overdue(loan.due_on + timedelta(days=1)) == 1


def test_loan_returned_early_has_zero_days_overdue():
    loan = Loan("S1", CLEAN_CODE, borrowed_on=START_DATE)
    assert loan.days_overdue(START_DATE + timedelta(days=3)) == 0


def test_member_with_no_loans_owes_nothing(library):
    assert library.calculate_late_fees("S1") == 0


def test_book_returned_on_time_has_no_fee(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(14)
    loan = library.return_book("S1", CLEAN_CODE)
    assert loan.fee_charged == 0


def test_student_is_charged_one_dollar_per_overdue_day(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(14 + 5)
    loan = library.return_book("S1", CLEAN_CODE)
    assert loan.fee_charged == 5.00


def test_fees_accrue_on_books_still_out(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(14 + 3)
    assert library.calculate_late_fees("S1") == 3.00


def test_total_fees_add_returned_and_outstanding_loans(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    library.borrow_book("S1", REFACTORING)
    clock.advance(16)
    library.return_book("S1", CLEAN_CODE)
    clock.advance(2)
    assert library.calculate_late_fees("S1") == 2.00 + 4.00


def test_fees_belong_only_to_the_member_who_was_late(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(20)
    assert library.calculate_late_fees("S2") == 0


@pytest.mark.parametrize("member_id, expected", [("S1", 4.00), ("F1", 2.00), ("P1", 6.00)])
def test_late_fee_rate_depends_on_member_category(library, clock, member_id, expected):
    library.borrow_book(member_id, CLEAN_CODE)
    clock.advance(18)
    assert library.return_book(member_id, CLEAN_CODE).fee_charged == expected


def test_get_overdue_loans_lists_only_late_active_loans(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(10)
    library.borrow_book("S2", REFACTORING)
    clock.advance(5)
    assert [loan.member_id for loan in library.get_overdue_loans()] == ["S1"]


def test_returned_loans_are_not_overdue(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(20)
    library.return_book("S1", CLEAN_CODE)
    assert library.get_overdue_loans() == []
