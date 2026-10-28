"""Advanced feature 1: late fees ($1/day for students, due 14 days after borrowing)."""

from datetime import timedelta

from src.loan import Loan
from tests.conftest import CLEAN_CODE, START_DATE


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
