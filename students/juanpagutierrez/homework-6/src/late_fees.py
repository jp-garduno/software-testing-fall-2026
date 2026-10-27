"""Due dates and overdue fees."""

from datetime import timedelta

LOAN_PERIOD = timedelta(days=14)


def due_date_for(borrowed_on):
    """Return the date a loan that starts on ``borrowed_on`` must be returned."""
    return borrowed_on + LOAN_PERIOD
