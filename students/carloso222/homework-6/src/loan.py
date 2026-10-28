"""Loan record: one borrow of one book by one member."""

from dataclasses import dataclass
from datetime import date, timedelta

LOAN_PERIOD_DAYS = 14


@dataclass
class Loan:
    """A borrow event; returned_on stays None while the book is out."""

    member_id: str
    isbn: str
    borrowed_on: date
    returned_on: date = None
    fee_charged: float = 0.0

    @property
    def due_on(self):
        """Books are due 14 days after they are borrowed."""
        return self.borrowed_on + timedelta(days=LOAN_PERIOD_DAYS)

    @property
    def is_active(self):
        """True while the book has not been returned."""
        return self.returned_on is None

    def days_overdue(self, as_of):
        """Whole days past the due date on the given day (never negative)."""
        return max(0, (as_of - self.due_on).days)
