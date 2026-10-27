"""Due dates and overdue fees."""

from datetime import timedelta
from decimal import Decimal

LOAN_PERIOD = timedelta(days=14)
STANDARD_DAILY_FEE = Decimal("1.00")


def due_date_for(borrowed_on):
    """Return the date a loan that starts on ``borrowed_on`` must be returned."""
    return borrowed_on + LOAN_PERIOD


def calculate_late_fee(due_date, returned_on):
    """Return the fee owed for a copy due on ``due_date`` and returned on ``returned_on``."""
    days_late = max((returned_on - due_date).days, 0)
    return days_late * STANDARD_DAILY_FEE
