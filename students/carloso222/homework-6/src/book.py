"""Book entity: a title in the catalog with a number of physical copies."""

from src.exceptions import AllCopiesReturnedError, InvalidBookError, NoCopiesAvailableError

VALID_ISBN_LENGTHS = (10, 13)


class Book:
    """A catalog entry that tracks how many of its copies are on the shelf."""

    def __init__(
        self,
        isbn,
        title,
        author,
        total_copies=1,
        genre=None,
        year=None,
        rating=None,
    ):
        self.isbn = self._validate_isbn(isbn)
        self.title = self._validate_title(title)
        self.author = author
        self.total_copies = self._validate_copies(total_copies)
        self.available_copies = self.total_copies
        self.genre = genre
        self.year = year
        self.rating = rating

    @staticmethod
    def _validate_isbn(isbn):
        if not isinstance(isbn, str) or not isbn.isdigit():
            raise InvalidBookError("ISBN must contain only digits")
        if len(isbn) not in VALID_ISBN_LENGTHS:
            raise InvalidBookError("ISBN must be 10 or 13 digits")
        return isbn

    @staticmethod
    def _validate_title(title):
        if not title or not title.strip():
            raise InvalidBookError("Title is required")
        return title.strip()

    @staticmethod
    def _validate_copies(total_copies):
        if total_copies < 0:
            raise InvalidBookError("Copies cannot be negative")
        return total_copies

    def is_available(self):
        """Return True when at least one copy is on the shelf."""
        return self.available_copies > 0

    def borrow(self):
        """Take one copy off the shelf."""
        if not self.is_available():
            raise NoCopiesAvailableError(f"No copies of '{self.title}' available")
        self.available_copies -= 1

    def return_copy(self):
        """Put one copy back on the shelf."""
        if self.available_copies >= self.total_copies:
            raise AllCopiesReturnedError(f"All copies of '{self.title}' are already in")
        self.available_copies += 1

    def __repr__(self):
        return f"Book(isbn={self.isbn!r}, title={self.title!r})"
