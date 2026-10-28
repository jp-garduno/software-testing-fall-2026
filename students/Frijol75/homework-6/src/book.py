"""Book entity for the Library Management System."""
from typing import Optional


class Book:
    """Represents a book in the library catalog."""

    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        total_copies: int = 1,
    ) -> None:
        if not (isinstance(isbn, str) and isbn.isdigit() and len(isbn) in (10, 13)):
            raise ValueError("ISBN must be 10 or 13 digits")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required")
        if not isinstance(total_copies, int) or total_copies < 0:
            raise ValueError("Total copies must be non-negative")
        self.isbn = isbn
        self.title = title.strip()
        self.author = author.strip() if isinstance(author, str) else author
        self.total_copies = total_copies
        self.available_copies = total_copies
