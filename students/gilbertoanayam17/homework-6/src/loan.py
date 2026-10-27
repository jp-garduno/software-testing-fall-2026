"""Loan: one copy lent to one member, when it is due and what lateness costs."""

from datetime import timedelta

LOAN_PERIOD = timedelta(days=14)
DAILY_LATE_FEE = 1.0


class Loan:
    """A copy of a book lent to a member on a given date, due LOAN_PERIOD later."""

    def __init__(self, member_id, isbn, borrowed_on):
        self.member_id = member_id
        self.isbn = isbn
        self.due_date = borrowed_on + LOAN_PERIOD

    def days_overdue(self, on_date):
        """Return how many days past the due date `on_date` falls; zero until then."""
        return max(0, (on_date - self.due_date).days)

    def late_fee(self, on_date):
        """Return the fee owed if the copy comes back on `on_date`."""
        return self.days_overdue(on_date) * DAILY_LATE_FEE
