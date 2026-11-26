"""Book model for the library."""

from src.errors import LibraryError


def _validate_isbn(isbn):
    """Reject ISBNs that are not 10 or 13 digits."""
    if not isbn.isdigit() or len(isbn) not in (10, 13):
        raise ValueError("ISBN must have 10 or 13 digits")


def _validate_title(title):
    """Reject empty or blank titles."""
    if not title or not title.strip():
        raise ValueError("Title is required")


def _validate_copies(copies):
    """Reject negative copy counts."""
    if copies < 0:
        raise ValueError("Copies cannot be negative")


class Book:
    """A book in the catalog."""

    def __init__(self, isbn, title, author, copies=1):
        _validate_isbn(isbn)
        _validate_title(title)
        _validate_copies(copies)
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

    def is_available(self):
        """Return True when at least one copy can be borrowed."""
        return self.available_copies > 0

    def borrow(self):
        """Take one copy off the shelf."""
        if not self.is_available():
            raise LibraryError("No copies available")
        self.available_copies -= 1

    def return_copy(self):
        """Put one copy back on the shelf."""
        if self.available_copies >= self.total_copies:
            raise LibraryError("All copies are already in the library")
        self.available_copies += 1
