"""A single lending of one copy of a book to one member."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Loan:
    """Who borrowed which book, when, and when it came back."""

    member_id: str
    isbn: str
    borrowed_on: date
    due_date: date
    returned_on: Optional[date] = None
