"""Catalog, member registration, and library operations."""


class Library:
    """Coordinate inventory and member loans."""

    def __init__(self):
        self.catalog = {}
        self.members = {}

    def add_book(self, book):
        """Add a new ISBN to the catalog."""
        self.catalog[book.isbn] = book

    def register_member(self, member):
        """Register a new member identity."""
        self.members[member.member_id] = member
