"""Library domain model."""


class Library:
    """Library behavior developed test first."""

    def __init__(self):
        self.catalog = {}
        self.members = {}

    def add_book(self, book):
        self.catalog[book.isbn] = book
