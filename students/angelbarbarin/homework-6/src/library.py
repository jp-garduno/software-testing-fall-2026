"""Library catalog and lending operations."""

from collections import defaultdict
from datetime import date
from decimal import Decimal

from exceptions import (
    AlreadyBorrowedError,
    BookNotFoundError,
    BorrowLimitExceededError,
    MemberNotFoundError,
    ReservationError,
)
from loan import Loan
from reservation import ReservationQueue


class NullNotifier:
    """Notifier used when the library has no notification channel."""

    def notify(self, member_id, book):
        """Ignore the notification."""


class Library:
    """Coordinates the catalog, the members and their loans."""

    def __init__(self, clock=date.today, notifier=None):
        self._books = {}
        self._members = {}
        self._loans = {}
        self._clock = clock
        self._charged_fees = defaultdict(Decimal)
        self._reservations = ReservationQueue()
        self._notifier = notifier or NullNotifier()

    def add_book(self, book):
        self._books[book.isbn] = book

    def get_book(self, isbn):
        return self._lookup(self._books, isbn, BookNotFoundError)

    def register_member(self, member):
        self._members[member.member_id] = member

    def get_member(self, member_id):
        return self._lookup(self._members, member_id, MemberNotFoundError)

    def borrow_book(self, member_id, isbn):
        book = self.get_book(isbn)
        member = self.get_member(member_id)
        self._ensure_can_borrow(member, isbn)
        book.borrow()
        member.add_borrowed_book(isbn)
        self._loans[(member_id, isbn)] = Loan(member_id, isbn, self._clock())

    def get_loan(self, member_id, isbn):
        return self._loans[(member_id, isbn)]

    def calculate_late_fee(self, member_id, isbn):
        loan = self.get_loan(member_id, isbn)
        daily_fee = self.get_member(member_id).daily_late_fee
        return loan.days_overdue(self._clock()) * daily_fee

    def return_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        member.return_book(isbn)
        book.return_copy()
        self._close_loan(member_id, isbn)
        next_member = self._reservations.pop_next(isbn)
        if next_member is not None:
            self._notifier.notify(next_member, book)

    def total_fees_for_member(self, member_id):
        member = self.get_member(member_id)
        fees = (
            self.calculate_late_fee(member_id, isbn) for isbn in member.borrowed_books
        )
        return sum(fees, self._charged_fees[member_id])

    def reserve_book(self, member_id, isbn):
        self.get_member(member_id)
        if self.get_book(isbn).is_available():
            raise ReservationError(f"{isbn} has copies available, borrow it instead")
        self._reservations.add(isbn, member_id)

    def reservations_for(self, isbn):
        return self._reservations.members_waiting(isbn)

    def search_by_title(self, title):
        return self._search("title", title)

    def search_by_author(self, author):
        return self._search("author", author)

    def get_available_books(self):
        return [book for book in self._books.values() if book.is_available()]

    def _search(self, field, term):
        term = term.lower()
        return [b for b in self._books.values() if term in getattr(b, field).lower()]

    def _close_loan(self, member_id, isbn):
        self._charged_fees[member_id] += self.calculate_late_fee(member_id, isbn)
        del self._loans[(member_id, isbn)]

    @staticmethod
    def _ensure_can_borrow(member, isbn):
        if isbn in member.borrowed_books:
            raise AlreadyBorrowedError(f"{member.name} already has {isbn}")
        if not member.can_borrow():
            raise BorrowLimitExceededError(f"{member.name} reached the borrow limit")

    @staticmethod
    def _lookup(registry, key, error):
        if key not in registry:
            raise error(f"{key} was not found")
        return registry[key]
