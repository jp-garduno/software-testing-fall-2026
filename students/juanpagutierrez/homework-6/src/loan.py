"""A single lending of one copy of a book to one member."""

from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.late_fees import calculate_late_fee


@dataclass
class Loan:
    """Who borrowed which book, when, and when it came back."""

    member_id: str
    isbn: str
    borrowed_on: date
    due_date: date
    returned_on: Optional[date] = None

    @property
    def is_open(self):
        """True while the copy has not come back."""
        return self.returned_on is None

    def late_fee(self, today, daily_rate):
        """Fee owed for this loan, counting up to today while it is still open."""
        end = today if self.is_open else self.returned_on
        return calculate_late_fee(self.due_date, end, daily_rate)
