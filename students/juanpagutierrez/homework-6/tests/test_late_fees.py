"""Tests for late fee calculation (advanced feature 1)."""

from datetime import date

from src.late_fees import due_date_for


def test_due_date_is_fourteen_days_after_borrowing():
    assert due_date_for(date(2026, 3, 1)) == date(2026, 3, 15)
