"""Dated loan records and fee calculation."""
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal


@dataclass(frozen=True)
class Loan:
    """Immutable record of one borrowing event."""

    member_id: str
    isbn: str
    borrowed_on: date

    @property
    def due_date(self):
        return self.borrowed_on + timedelta(days=14)

    def late_fee(self, as_of):
        return Decimal(max(0, (as_of - self.due_date).days))
