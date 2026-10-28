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
        if book.isbn in self.catalog:
            raise ValueError('ISBN already registered')
        self.catalog[book.isbn] = book

    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError('Member already registered')
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        member, book = self._participants(member_id, isbn)
        if not member.can_borrow():
            raise ValueError('Borrow limit reached')
        if isbn in member.borrowed_books:
            raise ValueError('Book already borrowed by this member')
        book.borrow()
        member.add_borrowed_book(isbn)
        loan = Loan(member_id, isbn, self._today(), daily_rate=member.daily_fee_rate)
        self._loans.append(loan)
        return loan

    def return_book(self, member_id, isbn):
        member, book = self._participants(member_id, isbn)
        member.return_book(isbn)
        book.return_copy()
        index = next(i for i, loan in enumerate(self._loans)
                     if loan.member_id == member_id and loan.isbn == isbn and loan.returned_on is None)
        self._loans[index] = replace(self._loans[index], returned_on=self._today())

    def _participants(self, member_id, isbn):
        if member_id not in self.members:
            raise ValueError('Unknown member')
        if isbn not in self.catalog:
            raise ValueError('Unknown book')
        return self.members[member_id], self.catalog[isbn]

    def search_by_title(self, title):
        query = title.strip().casefold()
        return [book for book in self.catalog.values() if query in book.title.casefold()]

    def search_by_author(self, author):
        query = author.strip().casefold()
        return [book for book in self.catalog.values() if query in book.author.casefold()]

    def get_available_books(self):
        return [book for book in self.catalog.values() if book.is_available()]

    def get_member_history(self, member_id):
        if member_id not in self.members:
            raise ValueError('Unknown member')
        return tuple(loan for loan in self._loans if loan.member_id == member_id)

    def calculate_total_fees(self, member_id):
        return sum((loan.late_fee(self._today()) for loan in self.get_member_history(member_id)), Decimal('0'))

    def most_borrowed_book(self):
        if not self._loans:
            return None
        counts = Counter(loan.isbn for loan in self._loans)
        return self.catalog[counts.most_common(1)[0][0]]
