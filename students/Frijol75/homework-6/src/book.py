"""Book entity for the Library Management System."""
from typing import Any, Optional


class Book:
    """Represents a book in the library catalog."""

    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        total_copies: int = 1,
        genre: Optional[str] = None,
        year: Optional[int] = None,
        rating: Optional[float] = None,
    ) -> None:
        self._validate_isbn(isbn)
        self._validate_title(title)
        self._validate_total_copies(total_copies)

        self.isbn = isbn
        self.title = title.strip()
        self.author = author.strip() if isinstance(author, str) else author
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.genre = genre.strip() if isinstance(genre, str) else genre
        self.year = year
        self.rating = rating

    def is_available(self) -> bool:
        """Check if at least one copy is currently available."""
        return self.available_copies > 0

    def borrow(self) -> None:
        """Borrow one copy of the book."""
        if not self.is_available():
            raise ValueError("No copies available to borrow")
        self.available_copies -= 1

    def return_copy(self) -> None:
        """Return one borrowed copy of the book."""
        if self.available_copies >= self.total_copies:
            raise ValueError("Cannot return more copies than total copies")
        self.available_copies += 1

    def __repr__(self) -> str:
        return f"<Book ISBN={self.isbn} Title='{self.title}'>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn and self.title == other.title and self.author == other.author

    def __hash__(self) -> int:
        return hash(self.isbn)

    @staticmethod
    def _validate_isbn(isbn: str) -> None:
        if not (isinstance(isbn, str) and isbn.isdigit() and len(isbn) in (10, 13)):
            raise ValueError("ISBN must be 10 or 13 digits")

    @staticmethod
    def _validate_title(title: str) -> None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required")

    @staticmethod
    def _validate_total_copies(total_copies: int) -> None:
        if not isinstance(total_copies, int) or total_copies < 0:
            raise ValueError("Total copies must be non-negative")
