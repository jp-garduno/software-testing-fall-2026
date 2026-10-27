"""Library facade: catalog, members and lending rules."""


class Library:
    """Coordinates books and members."""

    def __init__(self):
        self._books = {}

    def add_book(self, book):
        """Add ``book`` to the catalog."""
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for ``isbn``."""
        return self._books[isbn]
