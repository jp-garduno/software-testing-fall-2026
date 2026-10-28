"""Library domain model."""


class Library:
    """Library behavior developed test first."""

    def __init__(self):
        self.catalog = {}
        self.members = {}

    def add_book(self, book):
        if book.isbn in self.catalog:
            raise ValueError('ISBN already registered')
        self.catalog[book.isbn] = book
