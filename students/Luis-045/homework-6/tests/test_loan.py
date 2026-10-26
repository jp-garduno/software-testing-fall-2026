"""Tests for loan dates and late fees."""

from datetime import date

from src.loan import Loan


def test_loan_due_date_is_fourteen_days_after_borrowing():
    loan = Loan("m1", "1234567890", date(2026, 10, 1))
    assert loan.due_date == date(2026, 10, 15)
