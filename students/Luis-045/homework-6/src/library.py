"""Catalog, member registration, and library operations."""


class Library:
    """Coordinate inventory and member loans."""

    def __init__(self):
        self.catalog = {}
        self.members = {}

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
