"""Loan models and fee calculation logic."""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class LoanRecord:
    """Tracks an individual loan of a book by a member."""

    loan_id: str
    member_id: str
    isbn: str
    borrow_date: date
    due_date: Optional[date] = None
    return_date: Optional[date] = None

    def __post_init__(self) -> None:
        if self.due_date is None:
            self.due_date = self.borrow_date + timedelta(days=14)


def calculate_late_fee(
    loan: LoanRecord,
    return_date: Optional[date] = None,
    daily_rate: float = 1.0,
) -> float:
    """Calculate the late fee for a loan given an actual return or check date."""
    effective_return = return_date or loan.return_date or date.today()
    if loan.due_date is None or effective_return <= loan.due_date:
        return 0.0
    days_overdue = (effective_return - loan.due_date).days
    return float(days_overdue * daily_rate)
