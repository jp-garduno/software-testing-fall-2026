"""Catalog, member registration, and library operations."""

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
        member.return_book(isbn)
        book.return_copy()

    def search_by_title(self, title):
        """Find titles containing a case-insensitive query."""
        return self._search("title", title)

    def search_by_author(self, author):
        """Find authors containing a case-insensitive query."""
        return self._search("author", author)

    def _search(self, field, query):
        return [book for book in self.catalog.values()
                if query.casefold() in getattr(book, field).casefold()]

    def get_available_books(self):
        """List catalog entries with at least one free copy."""
        return [book for book in self.catalog.values() if book.is_available()]

    def get_due_date(self, member_id, isbn):
        """Get the due date of a current loan."""
        return next(loan for loan in self._loans
                    if loan.member_id == member_id and loan.isbn == isbn).due_date
