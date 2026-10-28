"""Dated loan records and fee calculation."""

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

LOAN_PERIOD_DAYS = 14


@dataclass(frozen=True)
class Loan:
    """Immutable record of one borrowing event."""

    member_id: str
    isbn: str
    borrowed_on: date
    returned_on: date | None = None
    daily_rate: Decimal = Decimal("1")

    @property
    def due_date(self):
        """Return the borrowing date plus the standard loan period."""
        return self.borrowed_on + timedelta(days=LOAN_PERIOD_DAYS)

    def late_fee(self, as_of):
        """Charge overdue calendar days through as_of or the earlier return."""
        end_date = min(as_of, self.returned_on) if self.returned_on else as_of
        return Decimal(max(0, (end_date - self.due_date).days)) * self.daily_rate
