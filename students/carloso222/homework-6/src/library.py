"""Library: catalog, members, loans, reservations, search and reports."""

from datetime import date

from src.exceptions import (
    AlreadyBorrowedError,
    BookNotBorrowedError,
    BookNotFoundError,
    BorrowLimitReachedError,
    DuplicateBookError,
    DuplicateMemberError,
    MemberNotFoundError,
    ReservationError,
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
        self._reservations = {}

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

    def return_book(self, member_id, isbn):
        """Take the book back and charge any late fee."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        loan = self._active_loan(member_id, isbn)
        today = self._clock()
        loan.returned_on = today
        loan.fee_charged = loan.days_overdue(today) * member.daily_late_fee
        member.return_book(isbn)
        book.return_copy()
        return loan

    def _active_loan(self, member_id, isbn):
        for loan in self._loans:
            if loan.member_id == member_id and loan.isbn == isbn and loan.is_active:
                return loan
        raise BookNotBorrowedError(f"Member {member_id} has not borrowed {isbn}")

    # ----- search ------------------------------------------------------------

    def search_by_title(self, title):
        """Case-insensitive partial match on title."""
        needle = title.lower()
        return [book for book in self._books.values() if needle in book.title.lower()]

    def search_by_author(self, author):
        """Case-insensitive partial match on author."""
        needle = author.lower()
        return [book for book in self._books.values() if needle in book.author.lower()]

    def get_available_books(self):
        """Every book with at least one copy on the shelf."""
        return [book for book in self._books.values() if book.is_available()]

    # ----- late fees ---------------------------------------------------------

    def calculate_late_fees(self, member_id):
        """Fees already charged on returns plus fees accruing on overdue loans."""
        member = self.get_member(member_id)
        today = self._clock()
        total = 0.0
        for loan in self._loans:
            if loan.member_id != member_id:
                continue
            if loan.is_active:
                total += loan.days_overdue(today) * member.daily_late_fee
            else:
                total += loan.fee_charged
        return total

    def get_overdue_loans(self):
        """Active loans whose due date has passed."""
        today = self._clock()
        return [loan for loan in self._loans if loan.is_active and loan.days_overdue(today) > 0]

    # ----- reservations ------------------------------------------------------

    def reserve_book(self, member_id, isbn):
        """Queue the member for a book that has no copies on the shelf."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        if book.is_available():
            raise ReservationError(f"'{book.title}' is available; borrow it instead")
        if member.has_borrowed(isbn):
            raise ReservationError(f"{member.name} already has '{book.title}'")
        queue = self._reservations.setdefault(isbn, [])
        if member_id in queue:
            raise ReservationError(f"{member.name} already reserved '{book.title}'")
        queue.append(member_id)
        return len(queue)

    def get_reservation_queue(self, isbn):
        """Member IDs waiting for this book, first in line first."""
        return list(self._reservations.get(isbn, []))
