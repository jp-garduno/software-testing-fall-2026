"""Book entity: a title in the catalog with a number of physical copies."""

from src.exceptions import InvalidBookError


class Book:
    """A catalog entry that tracks how many of its copies are on the shelf."""

    def __init__(self, isbn, title, author, total_copies=1):
        if not isinstance(isbn, str) or not isbn.isdigit():
            raise InvalidBookError("ISBN must contain only digits")
        if len(isbn) not in (10, 13):
            raise InvalidBookError("ISBN must be 10 or 13 digits")
        if not title or not title.strip():
            raise InvalidBookError("Title is required")
        if total_copies < 0:
            raise InvalidBookError("Copies cannot be negative")
        self.isbn = isbn
        self.title = title.strip()
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self):
        """Return True when at least one copy is on the shelf."""
        return self.available_copies > 0
