"""Member categories with their own borrow limits and late fee rates."""

from enum import Enum


class MemberCategory(Enum):
    """Each category is (borrow_limit, daily_late_fee)."""

    STUDENT = (3, 1.00)
    FACULTY = (5, 0.50)
    PUBLIC = (2, 1.50)

    def __init__(self, borrow_limit, daily_late_fee):
        self.borrow_limit = borrow_limit
        self.daily_late_fee = daily_late_fee
