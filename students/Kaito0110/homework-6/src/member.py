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
