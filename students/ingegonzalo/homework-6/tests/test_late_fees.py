from datetime import date

from src.late_fees import calculate_late_fee

def test_no_fee_when_returned_on_due_date():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 15)) == 0

def test_fee_is_one_dollar_per_day_overdue():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 18)) == 3

def test_no_negative_fee_when_returned_early():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 5)) == 0

def test_fee_uses_custom_daily_rate():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 18), daily_rate=2) == 6