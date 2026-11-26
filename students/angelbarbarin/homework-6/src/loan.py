"""Loan of a book copy to a member."""

from dataclasses import dataclass
from datetime import date, timedelta

LOAN_PERIOD = timedelta(days=14)


@dataclass(frozen=True)
class Loan:
    """A copy of a book lent to a member on a given day."""

    member_id: str
    isbn: str
    borrowed_on: date

    @property
    def due_date(self):
        return self.borrowed_on + LOAN_PERIOD

    def days_overdue(self, today):
        return max(0, (today - self.due_date).days)
