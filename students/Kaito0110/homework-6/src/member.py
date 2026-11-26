"""Member model for the Library Management System."""

CATEGORY_CONFIG = {
    "student": {"max_borrow_limit": 3, "late_fee_rate": 1.0},
    "faculty": {"max_borrow_limit": 5, "late_fee_rate": 0.5},
    "public": {"max_borrow_limit": 2, "late_fee_rate": 2.0},
}


class Member:
    """Represents a registered library member."""

    def __init__(self, member_id, name, max_borrow_limit=None, category="student"):
        if not member_id or not member_id.strip():
            raise ValueError("Member ID cannot be empty")

        if not name or not name.strip():
            raise ValueError("Member name cannot be empty")

        normalized_category = category.lower() if isinstance(category, str) else ""
        if normalized_category not in CATEGORY_CONFIG:
            raise ValueError("Invalid member category")

        if max_borrow_limit is None:
            max_borrow_limit = CATEGORY_CONFIG[normalized_category]["max_borrow_limit"]

        if max_borrow_limit < 0:
            raise ValueError("Invalid borrowing limit")

        self.member_id = member_id
        self.name = name
        self.category = normalized_category
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit
        self.late_fee_rate = CATEGORY_CONFIG[normalized_category]["late_fee_rate"]

    def can_borrow(self):
        """Return True if the member has not reached their borrowing limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        """Add an ISBN to the member's borrowed books list."""
        if not self.can_borrow():
            raise ValueError("Member has reached the borrowing limit")

        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        """Remove an ISBN from the member's borrowed books list."""
        if isbn not in self.borrowed_books:
            raise ValueError("Member has not borrowed this book")

        self.borrowed_books.remove(isbn)
