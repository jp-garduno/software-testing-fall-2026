"""Member entity: a registered person who borrows books."""

from src.exceptions import BookNotBorrowedError, BorrowLimitReachedError
from src.member_category import MemberCategory


class Member:
    """A library member with a borrow limit set by their category."""

    def __init__(self, member_id, name, category=MemberCategory.STUDENT, max_borrow_limit=None):
        self.member_id = member_id
        self.name = name
        self.category = category
        self.max_borrow_limit = (
            max_borrow_limit if max_borrow_limit is not None else category.borrow_limit
        )
        self.borrowed_books = []

    @property
    def daily_late_fee(self):
        """Late fee per overdue day for this member's category."""
        return self.category.daily_late_fee

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

    def has_borrowed(self, isbn):
        """Return True if the member currently holds this ISBN."""
        return isbn in self.borrowed_books

    def return_book(self, isbn):
        """Remove the ISBN from the member's borrowed books."""
        if not self.has_borrowed(isbn):
            raise BookNotBorrowedError(f"{self.name} has not borrowed {isbn}")
        self.borrowed_books.remove(isbn)

    def __repr__(self):
        return f"Member(member_id={self.member_id!r}, name={self.name!r})"
