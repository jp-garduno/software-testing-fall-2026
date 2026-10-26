"""Dated loan records."""

from dataclasses import dataclass
from datetime import date, timedelta


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
        return self.borrowed_on + timedelta(days=14)

    def fee_on(self, today):
        """Calculate the amount owed on the supplied date."""
        return (today - self.due_date).days
