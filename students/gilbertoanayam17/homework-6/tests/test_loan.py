"""Tests for Loan: due dates, overdue days and late fees."""

from datetime import date

from src.loan import Loan

BORROWED_ON = date(2026, 1, 1)


def test_should_be_due_fourteen_days_after_borrow_date():
    loan = Loan("M1", "1234567890", BORROWED_ON)

    assert loan.due_date == date(2026, 1, 15)
