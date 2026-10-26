"""Book model for Library Management System."""
import re


class Book:
    """Represents a book in the library catalog."""

    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        total_copies: int = 1,
    ) -> None:
        if not title or not str(title).strip():
            raise ValueError("Title is required")
        if not author or not str(author).strip():
            raise ValueError("Author is required")

        cleaned_isbn = re.sub(r"[\s-]", "", str(isbn))
        if not cleaned_isbn.isdigit() or len(cleaned_isbn) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 digits")

        if int(total_copies) < 0:
            raise ValueError("Total copies cannot be negative")

        self.isbn = cleaned_isbn
        self.title = str(title).strip()
        self.author = str(author).strip()
        self.total_copies = int(total_copies)
        self.available_copies = self.total_copies
