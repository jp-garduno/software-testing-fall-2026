"""Member model for Library Management System."""


class Member:
    """Represents a registered library member."""

    def __init__(
        self,
        member_id: str,
        name: str,
        max_borrow_limit: int = 3,
    ) -> None:
        if not member_id or not str(member_id).strip():
            raise ValueError("Member ID is required")
        if not name or not str(name).strip():
            raise ValueError("Member name is required")
        if int(max_borrow_limit) <= 0:
            raise ValueError("Max borrow limit must be positive")

        self.member_id = str(member_id).strip()
        self.name = str(name).strip()
        self.max_borrow_limit = int(max_borrow_limit)
        self.borrowed_books: list[str] = []

    def can_borrow(self) -> bool:
        """Return True if the member has not reached their borrow limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn: str) -> None:
        """Add an ISBN to the member's list of borrowed books."""
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        self.borrowed_books.append(str(isbn))

    def return_book(self, isbn: str) -> None:
        """Remove a borrowed book from the member's list."""
        cleaned_isbn = str(isbn)
        if cleaned_isbn not in self.borrowed_books:
            raise ValueError("Book was not borrowed by this member")
        self.borrowed_books.remove(cleaned_isbn)
