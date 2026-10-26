"""Dated loan records."""

from dataclasses import dataclass
from datetime import date, timedelta


LOAN_PERIOD_DAYS = 14
DAILY_LATE_FEE = 1


@dataclass(frozen=True)
class Loan:
    """An immutable record of one borrowing transaction."""

    member_id: str
    isbn: str
    borrowed_on: date
    returned_on: date | None = None

    @property
    def due_date(self):
        """The last date on which no late fee is owed."""
        return self.borrowed_on + timedelta(days=LOAN_PERIOD_DAYS)

    def fee_on(self, today):
        """Calculate the amount owed on the supplied date."""
        end_date = self.returned_on or today
        return max(0, (end_date - self.due_date).days) * DAILY_LATE_FEE
