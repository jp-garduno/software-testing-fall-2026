"""Member entity: a registered person who borrows books."""

from src.exceptions import BorrowLimitReachedError


class Member:
    """A library member with a borrow limit."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []

    def can_borrow(self):
        """Return True while the member is under their borrow limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        """Record that the member has borrowed the book with this ISBN."""
        if not self.can_borrow():
            raise BorrowLimitReachedError(
                f"{self.name} has reached the limit of {self.max_borrow_limit} books"
            )
        self.borrowed_books.append(isbn)
