from datetime import timedelta

LOAN_PERIOD_DAYS = 14


def calculate_late_fee(borrow_date, return_date, daily_rate=1):
    due_date = borrow_date + timedelta(days=LOAN_PERIOD_DAYS)
    days_late = (return_date - due_date).days
    return max(0, days_late) * daily_rate