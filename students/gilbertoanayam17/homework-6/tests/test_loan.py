"""Tests for Loan: due dates, overdue days and late fees."""

from datetime import date

import pytest

from src.loan import Loan

BORROWED_ON = date(2026, 1, 1)


def test_should_be_due_fourteen_days_after_borrow_date():
    loan = Loan("M1", "1234567890", BORROWED_ON)

    assert loan.due_date == date(2026, 1, 15)


def test_should_have_no_overdue_days_before_due_date():
    loan = Loan("M1", "1234567890", BORROWED_ON)

    assert loan.days_overdue(date(2026, 1, 10)) == 0


@pytest.mark.parametrize(
    "on_date, expected_days",
    [(date(2026, 1, 15), 0), (date(2026, 1, 16), 1), (date(2026, 1, 18), 3)],
    ids=["on-due-date", "one-day-late", "three-days-late"],
)
def test_should_count_days_past_due_date_as_overdue(on_date, expected_days):
    loan = Loan("M1", "1234567890", BORROWED_ON)

    assert loan.days_overdue(on_date) == expected_days
