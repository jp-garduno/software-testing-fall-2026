"""Member entity and categories for the Library Management System."""
from enum import Enum
from typing import Any, List, Optional


class MemberCategory(str, Enum):
    """Categories of library membership."""

    STUDENT = "STUDENT"
    FACULTY = "FACULTY"
    PUBLIC = "PUBLIC"


CATEGORY_CONFIG = {
    MemberCategory.STUDENT: {"max_limit": 3, "daily_rate": 0.50},
    MemberCategory.FACULTY: {"max_limit": 5, "daily_rate": 0.25},
    MemberCategory.PUBLIC: {"max_limit": 2, "daily_rate": 1.00},
}


class Member:
    """Represents a registered library member."""

    def __init__(
        self,
        member_id: str,
        name: str,
        max_borrow_limit: Optional[int] = None,
        category: Optional[MemberCategory] = None,
        daily_fee_rate: Optional[float] = None,
    ) -> None:
        if not isinstance(member_id, str) or not member_id.strip():
            raise ValueError("Member ID is required")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name is required")

        if category is not None:
            if isinstance(category, str):
                try:
                    category = MemberCategory(category)
                except ValueError:
                    raise ValueError("Invalid member category")
            elif not isinstance(category, MemberCategory):
                raise ValueError("Invalid member category")

            config = CATEGORY_CONFIG[category]
            limit = max_borrow_limit if max_borrow_limit is not None else config["max_limit"]
            rate = daily_fee_rate if daily_fee_rate is not None else config["daily_rate"]
        else:
            limit = max_borrow_limit if max_borrow_limit is not None else 3
            rate = daily_fee_rate if daily_fee_rate is not None else 1.0

        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Max borrow limit must be positive")
        if rate < 0:
            raise ValueError("Daily fee rate must be non-negative")

        self.member_id = member_id.strip()
        self.name = name.strip()
        self.category = category
        self.max_borrow_limit = limit
        self.daily_fee_rate = float(rate)
        self.borrowed_books: List[str] = []

    def can_borrow(self) -> bool:
        """Check if the member has not reached the borrow limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn: str) -> None:
        """Add an ISBN to the member's list of borrowed books."""
        if not isinstance(isbn, str) or not isbn.strip():
            raise ValueError("Invalid book identifier")
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        if isbn in self.borrowed_books:
            raise ValueError("Book already borrowed by this member")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn: str) -> None:
        """Remove an ISBN from the member's list of borrowed books."""
        if isbn not in self.borrowed_books:
            raise ValueError("Book not borrowed by this member")
        self.borrowed_books.remove(isbn)

    def __repr__(self) -> str:
        return f"<Member ID={self.member_id} Name='{self.name}' Borrowed={len(self.borrowed_books)}/{self.max_borrow_limit}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Member):
            return False
        return self.member_id == other.member_id and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.member_id)
