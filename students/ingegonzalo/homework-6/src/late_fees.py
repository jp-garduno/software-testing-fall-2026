from datetime import timedelta

LOAN_PERIOD_DAYS = 14


def calculate_late_fee(borrow_date, return_date):
    due_date = borrow_date + timedelta(days=LOAN_PERIOD_DAYS)
    return (return_date - due_date).days