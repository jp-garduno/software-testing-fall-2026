"""Library member who can borrow books."""

from decimal import Decimal
from enum import Enum

from src.exceptions import BorrowLimitExceededError
from src.validation import require_text


class MemberCategory(Enum):
    """Kinds of membership, each with its own borrow limit and late fee rate."""

    STUDENT = (3, "1.00")
    FACULTY = (5, "0.50")
    PUBLIC = (2, "1.50")

    @property
    def borrow_limit(self):
        """Maximum number of books a member of this category may hold."""
        return self.value[0]

    @property
    def daily_late_fee(self):
        """Fee charged per overdue day, as an exact Decimal amount."""
        return Decimal(self.value[1])


class Member:
    """A registered patron of the library."""

    def __init__(self, member_id, name, max_borrow_limit=None, category=MemberCategory.STUDENT):
        require_text(name, "Member name")
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.category = category
        self.max_borrow_limit = category.borrow_limit if max_borrow_limit is None else max_borrow_limit

    def add_borrowed_book(self, isbn):
        """Record that this member now holds a copy of ``isbn``."""
        if not self.can_borrow():
            raise BorrowLimitExceededError(f"{self.member_id} reached the limit of {self.max_borrow_limit}")
        self.borrowed_books.append(isbn)

    def can_borrow(self):
        """Return True while the member is below the borrow limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def return_book(self, isbn):
        """Remove ``isbn`` from the books this member holds."""
        if isbn not in self.borrowed_books:
            raise ValueError(f"{self.member_id} has not borrowed {isbn}")
        self.borrowed_books.remove(isbn)

    @property
    def daily_late_fee(self):
        """Fee this member pays per overdue day."""
        return self.category.daily_late_fee
