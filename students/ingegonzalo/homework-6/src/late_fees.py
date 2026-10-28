from datetime import timedelta

LOAN_PERIOD_DAYS = 14


def calculate_late_fee(borrow_date, return_date):
    days_late = (return_date - due_date).days
    return max(0, days_late)