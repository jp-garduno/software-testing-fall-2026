"""Tests for late fee calculation (advanced feature 1)."""

from datetime import date
from decimal import Decimal

from src.late_fees import calculate_late_fee, due_date_for


def test_due_date_is_fourteen_days_after_borrowing():
    assert due_date_for(date(2026, 3, 1)) == date(2026, 3, 15)


def test_no_fee_when_returned_on_the_due_date():
    assert calculate_late_fee(date(2026, 3, 15), date(2026, 3, 15)) == Decimal("0")


def test_one_dollar_per_day_overdue():
    assert calculate_late_fee(date(2026, 3, 15), date(2026, 3, 18)) == Decimal("3.00")


def test_early_return_has_no_fee():
    assert calculate_late_fee(date(2026, 3, 15), date(2026, 3, 10)) == Decimal("0")


def test_fee_uses_the_given_daily_rate():
    assert calculate_late_fee(date(2026, 3, 15), date(2026, 3, 19), Decimal("0.50")) == Decimal("2.00")
