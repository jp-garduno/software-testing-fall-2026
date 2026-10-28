from datetime import timedelta

LOAN_PERIOD_DAYS = 14
DEFAULT_DAILY_RATE = 1


def get_due_date(borrow_date):
    return borrow_date + timedelta(days=LOAN_PERIOD_DAYS)


def calculate_late_fee(borrow_date, return_date, daily_rate=DEFAULT_DAILY_RATE):
    days_late = (return_date - get_due_date(borrow_date)).days
    return max(0, days_late) * daily_rate