"""Membership categories with their borrowing rules."""

from enum import Enum


class MemberCategory(Enum):
    """Member types, valued by (borrow limit, daily late fee)."""

    STUDENT = (3, 1.0)
    FACULTY = (5, 0.5)
    PUBLIC = (2, 1.5)

    def __init__(self, borrow_limit, late_fee_rate):
        self.borrow_limit = borrow_limit
        self.late_fee_rate = late_fee_rate
