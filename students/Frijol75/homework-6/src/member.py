"""Member entity for the Library Management System."""
from typing import Any, List, Optional


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
