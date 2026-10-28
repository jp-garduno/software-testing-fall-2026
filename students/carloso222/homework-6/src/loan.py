"""Loan record: one borrow of one book by one member."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Loan:
    """A borrow event; returned_on stays None while the book is out."""

    member_id: str
    isbn: str
    borrowed_on: date
    returned_on: date = None

    @property
    def is_active(self):
        """True while the book has not been returned."""
        return self.returned_on is None
