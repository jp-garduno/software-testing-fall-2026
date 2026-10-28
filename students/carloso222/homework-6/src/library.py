"""Library: catalog, members, loans, reservations, search and reports."""

from datetime import date

from src.exceptions import (
    AlreadyBorrowedError,
    BookNotFoundError,
    BorrowLimitReachedError,
    DuplicateBookError,
    DuplicateMemberError,
    MemberNotFoundError,
)
from src.loan import Loan


class Library:
    """Coordinates books and members.

    ``clock`` returns today's date and ``notifier`` is called as
    ``notifier(member_id, isbn)`` when a reserved book comes back. Both are
    injected so tests can control time and observe notifications without
    sleeping or sending real messages.
    """

    def __init__(self, clock=date.today, notifier=None):
        self._clock = clock
        self._notifier = notifier
        self._books = {}
        self._members = {}
        self._loans = []

    # ----- catalog and members ---------------------------------------------

    def add_book(self, book):
        """Add a book to the catalog."""
        if book.isbn in self._books:
            raise DuplicateBookError(f"ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def register_member(self, member):
        """Register a new member."""
        if member.member_id in self._members:
            raise DuplicateMemberError(f"Member {member.member_id} is already registered")
        self._members[member.member_id] = member

    def get_book(self, isbn):
        """Return the book with this ISBN or raise BookNotFoundError."""
        try:
            return self._books[isbn]
        except KeyError as error:
            raise BookNotFoundError(f"No book with ISBN {isbn}") from error

    def get_member(self, member_id):
        """Return the member with this ID or raise MemberNotFoundError."""
        try:
            return self._members[member_id]
        except KeyError as error:
            raise MemberNotFoundError(f"No member with ID {member_id}") from error

    # ----- borrowing ---------------------------------------------------------

    def borrow_book(self, member_id, isbn):
        """Lend one copy of the book to the member and return the Loan."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        if member.has_borrowed(isbn):
            raise AlreadyBorrowedError(f"{member.name} already has {book.title}")
        if not member.can_borrow():
            raise BorrowLimitReachedError(f"{member.name} has reached their borrow limit")
        book.borrow()
        member.add_borrowed_book(isbn)
        loan = Loan(member_id=member_id, isbn=isbn, borrowed_on=self._clock())
        self._loans.append(loan)
        return loan
