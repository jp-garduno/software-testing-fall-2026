"""Tests for loan dates and late fees."""

from datetime import date

from src.loan import Loan


def test_loan_due_date_is_fourteen_days_after_borrowing():
    loan = Loan("m1", "1234567890", date(2026, 10, 1))
    assert loan.due_date == date(2026, 10, 15)


def test_loan_charges_one_dollar_for_each_overdue_day():
    loan = Loan("m1", "1234567890", date(2026, 10, 1))
    assert loan.fee_on(date(2026, 10, 18)) == 3


def test_loan_has_no_fee_before_the_due_date():
    loan = Loan("m1", "1234567890", date(2026, 10, 1))
    assert loan.fee_on(date(2026, 10, 10)) == 0


def test_loan_has_no_fee_on_its_due_date():
    loan = Loan("m1", "1234567890", date(2026, 10, 1))
    assert loan.fee_on(date(2026, 10, 15)) == 0


def test_returned_loan_fee_stops_growing():
    loan = Loan("m1", "1234567890", date(2026, 10, 1), returned_on=date(2026, 10, 16))
    assert loan.fee_on(date(2026, 10, 20)) == 1
