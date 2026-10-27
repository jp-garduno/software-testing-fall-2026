"""Library facade: catalog, members and lending rules."""

from src.exceptions import BookNotFoundError


class Library:
    """Coordinates books and members."""

    def __init__(self):
        self._books = {}

    def add_book(self, book):
        """Add ``book`` to the catalog."""
        if book.isbn in self._books:
            raise ValueError(f"A book with ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for ``isbn``."""
        if isbn not in self._books:
            raise BookNotFoundError(f"No book with ISBN {isbn}")
        return self._books[isbn]
