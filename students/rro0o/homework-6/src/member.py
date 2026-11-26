"""Library member model."""

from src.errors import LibraryError
from src.member_category import MemberCategory


class Member:
    """A registered library member."""

    def __init__(self, member_id, name, max_borrow_limit=None, category=MemberCategory.STUDENT):
        if not name or not name.strip():
            raise ValueError("Name is required")
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.category = category
        if max_borrow_limit is None:
            max_borrow_limit = category.borrow_limit
        self.max_borrow_limit = max_borrow_limit

    def can_borrow(self):
        """Return True while the member is under the borrow limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        """Record that the member borrowed the book with this ISBN."""
        if not self.can_borrow():
            raise LibraryError("Member reached the borrow limit")
        if isbn in self.borrowed_books:
            raise LibraryError("Member already borrowed this book")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        """Remove a book from the member's borrowed list."""
        if isbn not in self.borrowed_books:
            raise LibraryError("Member did not borrow this book")
        self.borrowed_books.remove(isbn)
