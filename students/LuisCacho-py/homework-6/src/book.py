"""Book model for Library Management System."""
import re


def _normalize_and_validate_isbn(isbn: str) -> str:
    cleaned = re.sub(r"[\s-]", "", str(isbn))
    if not cleaned.isdigit() or len(cleaned) not in (10, 13):
        raise ValueError("ISBN must be 10 or 13 digits")
    return cleaned


def _validate_non_empty_string(value: str, field_name: str) -> str:
    if not value or not str(value).strip():
        raise ValueError(f"{field_name} is required")
    return str(value).strip()


class Book:
    """Represents a book in the library catalog."""

    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        total_copies: int = 1,
    ) -> None:
        self.title = _validate_non_empty_string(title, "Title")
        self.author = _validate_non_empty_string(author, "Author")
        self.isbn = _normalize_and_validate_isbn(isbn)

        if int(total_copies) < 0:
            raise ValueError("Total copies cannot be negative")

        self.total_copies = int(total_copies)
        self.available_copies = self.total_copies

    def is_available(self) -> bool:
        """Return True if at least one copy is available."""
        return self.available_copies > 0

    def borrow(self) -> bool:
        """Borrow one copy of the book if available."""
        if not self.is_available():
            raise RuntimeError("No copies available for borrowing")
        self.available_copies -= 1
        return True

    def return_copy(self) -> None:
        """Return a borrowed copy to the catalog."""
        if self.available_copies >= self.total_copies:
            raise ValueError("Cannot return more copies than total copies owned")
        self.available_copies += 1
