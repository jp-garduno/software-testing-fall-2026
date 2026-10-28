"""Dated loan records and fee calculation."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Loan:
    """Immutable record of one borrowing event."""

    member_id: str
    isbn: str
    borrowed_on: date
