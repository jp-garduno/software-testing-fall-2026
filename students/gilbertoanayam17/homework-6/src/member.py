"""Member: who can borrow, how many books at once, and which books they hold."""

from enum import Enum

from . import errors


class MemberCategory(Enum):
    """Kinds of member, each with its own borrow limit."""

    STUDENT = 3
    FACULTY = 5
    PUBLIC = 2

    def __init__(self, borrow_limit):
        self.borrow_limit = borrow_limit


class Member:
    """A registered library user."""

    def __init__(self, member_id, name, max_borrow_limit=None, category=MemberCategory.STUDENT):
        self.member_id = member_id
        self.name = name
        self.category = category
        self.borrowed_books = []
        self.max_borrow_limit = category.borrow_limit if max_borrow_limit is None else max_borrow_limit

    def add_borrowed_book(self, isbn):
        """Record that the member took a copy of this book."""
        self.ensure_can_borrow()
        self.borrowed_books.append(isbn)

    def can_borrow(self):
        """Return True while the member holds fewer books than their limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def ensure_can_borrow(self):
        """Raise BorrowLimitExceededError if the member already holds as many books as allowed."""
        if not self.can_borrow():
            raise errors.BorrowLimitExceededError(f"{self.name} already holds {self.max_borrow_limit} books")

    def return_book(self, isbn):
        """Record that the member gave back their copy of this book."""
        if isbn not in self.borrowed_books:
            raise errors.InvalidReturnError(f"{self.name} does not hold {isbn}")
        self.borrowed_books.remove(isbn)
