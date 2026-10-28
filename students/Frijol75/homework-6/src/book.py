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
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
