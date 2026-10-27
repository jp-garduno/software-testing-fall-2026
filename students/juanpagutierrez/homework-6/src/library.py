"""Library facade: catalog, members and lending rules."""

from datetime import date
from decimal import Decimal

from src.exceptions import (
    BookNotFoundError,
    BookUnavailableError,
    BorrowLimitExceededError,
    MemberNotFoundError,
    ReservationError,
)
from src.history import history_report, most_borrowed_isbn
from src.late_fees import due_date_for
from src.loan import Loan


class Library:
    """Coordinates books and members."""

    def __init__(self, clock=date.today, notifier=None):
        self._clock = clock
        self._notifier = notifier
        self._reservations = {}
        self._holds = {}
        self._books = {}
        self._members = {}
        self._loans = []

    def add_book(self, book):
        """Add ``book`` to the catalog."""
        if book.isbn in self._books:
            raise ValueError(f"A book with ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for ``isbn``."""
        if isbn not in self._books:
            raise BookNotFoundError(f"No book with ISBN {isbn}")
        return self._books[isbn]

    def register_member(self, member):
        """Register ``member`` so they can borrow books."""
        if member.member_id in self._members:
            raise ValueError(f"Member {member.member_id} is already registered")
        self._members[member.member_id] = member

    def get_member(self, member_id):
        """Return the registered member with ``member_id``."""
        if member_id not in self._members:
            raise MemberNotFoundError(f"No member with id {member_id}")
        return self._members[member_id]

    def borrow_book(self, member_id, isbn):
        """Lend one copy of ``isbn`` to ``member_id``."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        if not member.can_borrow():
            raise BorrowLimitExceededError(f"{member_id} reached the limit of {member.max_borrow_limit}")
        holds = self._holds.get(isbn, [])
        if member_id not in holds and book.available_copies <= len(holds):
            raise BookUnavailableError(f"The free copies of {isbn} are held for members who reserved it")
        book.borrow()
        member.add_borrowed_book(isbn)
        if member_id in holds:
            holds.remove(member_id)
        today = self._clock()
        self._loans.append(Loan(member_id, isbn, today, due_date_for(today)))

    def get_loans(self, member_id):
        """Return every loan made to ``member_id``, oldest first."""
        return [loan for loan in self._loans if loan.member_id == member_id]

    def return_book(self, member_id, isbn):
        """Take back the copy of ``isbn`` lent to ``member_id``."""
        self.get_member(member_id).return_book(isbn)
        self.get_book(isbn).return_copy()
        self._open_loan(member_id, isbn).returned_on = self._clock()
        queue = self._reservations.get(isbn)
        if queue:
            next_member = queue.pop(0)
            self._holds.setdefault(isbn, []).append(next_member)
            self._notifier.notify(next_member, isbn)

    def _open_loan(self, member_id, isbn):
        return next(loan for loan in self.get_loans(member_id) if loan.isbn == isbn and loan.is_open)

    def search_by_title(self, title):
        """Return books whose title contains ``title`` (case-insensitive)."""
        return self._search(title, lambda book: book.title)

    def search_by_author(self, author):
        """Return books whose author contains ``author`` (case-insensitive)."""
        return self._search(author, lambda book: book.author)

    def _search(self, text, field):
        needle = text.lower()
        return [book for book in self._books.values() if needle in field(book).lower()]

    def get_available_books(self):
        """Return every book with at least one copy on the shelf."""
        return [book for book in self._books.values() if book.is_available()]

    def calculate_member_fees(self, member_id):
        """Total late fees ``member_id`` owes as of today."""
        today = self._clock()
        rate = self.get_member(member_id).daily_late_fee
        return sum((loan.late_fee(today, rate) for loan in self.get_loans(member_id)), Decimal("0"))

    def generate_history_report(self, member_id):
        """Return one line per loan ever made to ``member_id``, plus a summary."""
        return history_report(self.get_member(member_id), self.get_loans(member_id), self.get_book)

    def most_borrowed_book(self):
        """Return the book lent the most times, or None if nothing was lent."""
        isbn = most_borrowed_isbn(self._loans)
        return self.get_book(isbn) if isbn else None

    def borrow_count(self, isbn):
        """How many times ``isbn`` has been lent, returned or not."""
        return sum(1 for loan in self._loans if loan.isbn == isbn)

    def reserve_book(self, member_id, isbn):
        """Put ``member_id`` in line for the next free copy of ``isbn``."""
        if self.get_book(isbn).is_available():
            raise ReservationError(f"{isbn} has copies available; borrow it instead")
        if member_id in self.get_reservation_queue(isbn):
            raise ReservationError(f"{member_id} already reserved {isbn}")
        self._reservations.setdefault(isbn, []).append(member_id)

    def get_reservation_queue(self, isbn):
        """Member ids waiting for ``isbn``, first in line first."""
        return list(self._reservations.get(isbn, []))
