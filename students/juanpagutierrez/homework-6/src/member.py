"""Library member who can borrow books."""

from src.exceptions import BorrowLimitExceededError


class Member:
    """A registered patron of the library."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit

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
        self.borrowed_books.remove(isbn)
