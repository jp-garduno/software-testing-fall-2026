"""Library domain model."""
from collections import Counter
from dataclasses import replace
from datetime import date
from decimal import Decimal

from .loan import Loan


class Library:
    """Library behavior developed test first."""

    def __init__(self, today=date.today):
        self._today = today
        self.catalog = {}
        self.members = {}
        self._loans = []

    def add_book(self, book):
        """Register a book without replacing an existing ISBN."""
        if book.isbn in self.catalog:
            raise ValueError('ISBN already registered')
        self.catalog[book.isbn] = book

    def register_member(self, member):
        """Register a member without replacing an existing identity."""
        if member.member_id in self.members:
            raise ValueError('Member already registered')
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        """Borrow a copy and return an immutable dated loan record."""
        member, book = self._participants(member_id, isbn)
        member.validate_borrow(isbn)
        loan = Loan(member_id, isbn, self._today(), daily_rate=member.daily_fee_rate)
        book.borrow()
        member.add_borrowed_book(isbn)
        self._loans.append(loan)
        return loan

    def return_book(self, member_id, isbn):
        """Close an active loan and restore inventory and member capacity."""
        member, book = self._participants(member_id, isbn)
        index = next((i for i, loan in enumerate(self._loans)
                      if loan.member_id == member_id and loan.isbn == isbn and loan.returned_on is None), None)
        if index is None:
            raise ValueError('Book not borrowed by this member')
        returned_on = self._today()
        if self._loans[index].borrowed_on > returned_on:
            raise ValueError('Return date cannot be before borrowing date')
        member.return_book(isbn)
        book.return_copy()
        self._loans[index] = replace(self._loans[index], returned_on=returned_on)

    def _participants(self, member_id, isbn):
        if member_id not in self.members:
            raise ValueError('Unknown member')
        if isbn not in self.catalog:
            raise ValueError('Unknown book')
        return self.members[member_id], self.catalog[isbn]

    def search_by_title(self, title):
        """Match title substrings, ignoring case and outer whitespace."""
        query = title.strip().casefold()
        return [book for book in self.catalog.values() if query in book.title.casefold()]

    def search_by_author(self, author):
        """Match author substrings, ignoring case and outer whitespace."""
        query = author.strip().casefold()
        return [book for book in self.catalog.values() if query in book.author.casefold()]

    def get_available_books(self):
        """Return catalog books with at least one available copy."""
        return [book for book in self.catalog.values() if book.is_available()]

    def get_member_history(self, member_id):
        """Return chronological immutable loan snapshots for one member."""
        if member_id not in self.members:
            raise ValueError('Unknown member')
        return tuple(loan for loan in self._loans if loan.member_id == member_id)

    def calculate_total_fees(self, member_id):
        """Sum accrued fees for open and closed loans without recording payments."""
        as_of = self._today()
        return sum((loan.late_fee(as_of) for loan in self.get_member_history(member_id)), Decimal('0'))

    def most_borrowed_book(self):
        """Return the most borrowed book, breaking ties by first borrowing."""
        if not self._loans:
            return None
        counts = Counter(loan.isbn for loan in self._loans)
        return self.catalog[counts.most_common(1)[0][0]]
