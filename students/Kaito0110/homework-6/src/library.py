"""Library service managing catalog, members, loans, reservations, and history."""


class Library:
    """Coordinates books, members, borrowing, search, reservations, and fees."""

    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, book):
        """Add a new book to the catalog."""
        if book.isbn in self.books:
            raise ValueError("Book ISBN already exists")

        self.books[book.isbn] = book

    def register_member(self, member):
        """Register a new library member."""
        if member.member_id in self.members:
            raise ValueError("Member ID already exists")

        self.members[member.member_id] = member
