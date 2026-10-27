"""Library: the catalog, its members, and the loans between them."""


class Library:
    """Coordinates books and members so every loan follows the library's rules."""

    def __init__(self):
        self._books = {}

    def add_book(self, book):
        """Add a book to the catalog, indexed by its ISBN."""
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for this ISBN."""
        return self._books[isbn]
