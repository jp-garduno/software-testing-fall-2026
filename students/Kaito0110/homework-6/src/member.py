"""Member model for the Library Management System."""


class Member:
    """Represents a registered library member."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit

    def can_borrow(self):
        """Return True if the member has not reached their borrowing limit."""
        return len(self.borrowed_books) < self.max_borrow_limit
