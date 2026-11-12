"""Book entity of the library catalog."""

from dataclasses import dataclass
from typing import Optional

from src.exceptions import BookUnavailableError
from src.validation import require_text

VALID_ISBN_LENGTHS = (10, 13)


def _validate_isbn(isbn):
    if not isbn.isdigit() or len(isbn) not in VALID_ISBN_LENGTHS:
        raise ValueError(f"ISBN must have 10 or 13 digits, got {isbn!r}")



def _validate_copies(total_copies):
    if total_copies < 0:
        raise ValueError("Total copies cannot be negative")


@dataclass(frozen=True)
class BookDetails:
    """Optional descriptive data used by filtered search."""

    genre: Optional[str] = None
    publication_year: Optional[int] = None
    rating: Optional[float] = None

    def __post_init__(self):
        if self.rating is not None and not 0 <= self.rating <= 5:
            raise ValueError("Rating must be between 0 and 5")


class Book:
    """A title in the catalog, with one or more physical copies."""

    def __init__(self, isbn, title, author, total_copies=1, details=None):
        _validate_isbn(isbn)
        require_text(title, "Title")
        _validate_copies(total_copies)
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.details = details or BookDetails()

    @property
    def genre(self):
        """Genre from the book details, if known."""
        return self.details.genre

    @property
    def publication_year(self):
        """Publication year from the book details, if known."""
        return self.details.publication_year

    @property
    def rating(self):
        """Reader rating from 0 to 5, if known."""
        return self.details.rating

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
