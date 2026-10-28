"""Book domain entity."""


class Book:
    """A catalog book with identifying metadata and copies."""

    def __init__(self, isbn: str, title: str, author: str, copies: int = 1) -> None:
        if not (isbn.isdigit() and len(isbn) in (10, 13)):
            raise ValueError("ISBN must contain 10 or 13 digits")
        if not title.strip():
            raise ValueError("A title is required")
        if copies < 0:
            raise ValueError("copies cannot be negative")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

    def is_available(self) -> bool:
        """Return whether a copy can currently be borrowed."""
        return self.available_copies > 0
