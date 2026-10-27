"""Book entity of the library catalog."""

from src.exceptions import BookUnavailableError


class Book:
    """A title in the catalog, with one or more physical copies."""

    def __init__(self, isbn, title, author, total_copies=1):
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValueError(f"ISBN must have 10 or 13 digits, got {isbn!r}")
        if not title or not title.strip():
            raise ValueError("Title is required")
        if total_copies < 0:
            raise ValueError("Total copies cannot be negative")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self):
        """Return True while at least one copy is on the shelf."""
        return self.available_copies > 0

    def borrow(self):
        """Take one copy off the shelf."""
        if not self.is_available():
            raise BookUnavailableError(f"No copies of {self.isbn} are available")
        self.available_copies -= 1

    def return_copy(self):
        """Put one borrowed copy back on the shelf."""
        if self.available_copies >= self.total_copies:
            raise ValueError(f"All copies of {self.isbn} are already in the library")
        self.available_copies += 1
