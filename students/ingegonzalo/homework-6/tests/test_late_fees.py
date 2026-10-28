from datetime import date

from src.late_fees import calculate_late_fee

def test_no_fee_when_returned_on_due_date():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 15)) == 0