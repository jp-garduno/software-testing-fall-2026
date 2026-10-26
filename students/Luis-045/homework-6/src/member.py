"""Member identities and borrowing limits."""


class Member:
    """A library member and the ISBNs currently borrowed."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit

    def can_borrow(self):
        """Whether the member has room for another loan."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        """Record another book borrowed by this member."""
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        if isbn in self.borrowed_books:
            raise ValueError("Book already borrowed by this member")
        self.borrowed_books.append(isbn)
