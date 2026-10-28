"""Member entity for the Library Management System."""
from typing import List, Optional


class Member:
    """Represents a registered library member."""

    def __init__(
        self,
        member_id: str,
        name: str,
        max_borrow_limit: int = 3,
    ) -> None:
        if not isinstance(member_id, str) or not member_id.strip():
            raise ValueError("Member ID is required")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name is required")
        if not isinstance(max_borrow_limit, int) or max_borrow_limit <= 0:
            raise ValueError("Max borrow limit must be positive")

        self.member_id = member_id.strip()
        self.name = name.strip()
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books: List[str] = []
