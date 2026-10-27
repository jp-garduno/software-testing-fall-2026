"""Tests for late fee calculation (advanced feature 1)."""

from datetime import date
from decimal import Decimal

from src.late_fees import calculate_late_fee, due_date_for


def test_due_date_is_fourteen_days_after_borrowing():
    assert due_date_for(date(2026, 3, 1)) == date(2026, 3, 15)


def test_no_fee_when_returned_on_the_due_date():
    assert calculate_late_fee(date(2026, 3, 15), date(2026, 3, 15)) == Decimal("0")
