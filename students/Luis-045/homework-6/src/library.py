"""Catalog, member registration, and library operations."""

from collections import Counter
from dataclasses import replace
from datetime import date

from .loan import Loan


class Library:
    """Coordinate inventory and member loans."""

    def __init__(self, today=date.today):
        self.catalog = {}
        self.members = {}
        self._today = today
        self._loans = []

    def add_book(self, book):
        """Add a new ISBN to the catalog."""
        if book.isbn in self.catalog:
            raise ValueError("ISBN already in catalog")
        self.catalog[book.isbn] = book

    def register_member(self, member):
        """Register a new member identity."""
        if member.member_id in self.members:
            raise ValueError("Member ID already registered")
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        """Lend a catalog book to a registered member."""
        member = self.members[member_id]
        book = self.catalog[isbn]
        if not book.is_available():
            raise ValueError("No copies available")
        member.add_borrowed_book(isbn)
        book.borrow()
        self._loans.append(Loan(member_id, isbn, self._today()))

    def return_book(self, member_id, isbn):
        """Accept a book currently borrowed by this member."""
        member = self.members[member_id]
        book = self.catalog[isbn]
        loan = self._active_loan(member_id, isbn)
        member.return_book(isbn)
        book.return_copy()
        self._loans[self._loans.index(loan)] = replace(loan, returned_on=self._today())

    def search_by_title(self, title):
        """Find titles containing a case-insensitive query."""
        return self._search("title", title)

    def search_by_author(self, author):
        """Find authors containing a case-insensitive query."""
        return self._search("author", author)

    def _search(self, field, query):
        return [
            book
            for book in self.catalog.values()
            if query.casefold() in getattr(book, field).casefold()
        ]

    def get_available_books(self):
        """List catalog entries with at least one free copy."""
        return [book for book in self.catalog.values() if book.is_available()]

    def get_due_date(self, member_id, isbn):
        """Get the due date of a current loan."""
        return self._active_loan(member_id, isbn).due_date

    def _active_loan(self, member_id, isbn):
        for loan in self._loans:
            if (
                loan.member_id == member_id
                and loan.isbn == isbn
                and loan.returned_on is None
            ):
                return loan
        raise ValueError("No active loan for this member and ISBN")

    def calculate_late_fees(self, member_id):
        """Total accrued fees, including previously returned loans."""
        member = self.members[member_id]
        return sum(
            loan.fee_on(self._today())
            for loan in self._loans
            if loan.member_id == member.member_id
        )

    def search_with_filters(
        self, *, genre=None, publication_year=None, min_rating=None, sort_by="title"
    ):
        """Filter the catalog using book metadata."""
        if sort_by not in ("title", "author", "isbn", "publication_year", "rating"):
            raise ValueError("Unknown sort field")
        books = list(self.catalog.values())
        if genre is not None:
            books = [
                book
                for book in books
                if book.metadata.get("genre", "").casefold() == genre.casefold()
            ]
        if publication_year is not None:
            books = [
                book
                for book in books
                if book.metadata.get("publication_year") == publication_year
            ]
        if min_rating is not None:
            books = [
                book for book in books if book.metadata.get("rating", -1) >= min_rating
            ]
        return sorted(
            books,
            key=lambda book: (
                (
                    getattr(book, sort_by).casefold()
                    if sort_by in ("title", "author", "isbn")
                    else book.metadata.get(sort_by, 0)
                ),
                book.isbn,
            ),
        )

    def get_member_history(self, member_id):
        """Report this member's loans in borrowing order."""
        member = self.members[member_id]
        return tuple(loan for loan in self._loans if loan.member_id == member.member_id)

    def most_borrowed_book(self):
        """Return the most borrowed ISBN, breaking ties by first loan."""
        counts = Counter(loan.isbn for loan in self._loans)
        return counts.most_common(1)[0][0] if counts else None
