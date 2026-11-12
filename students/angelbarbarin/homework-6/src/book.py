"""Book entity of the library catalog."""

from exceptions import BookNotAvailableError, InvalidReturnError

VALID_ISBN_LENGTHS = (10, 13)


class Book:
    """A title in the catalog with a number of physical copies."""

    def __init__(self, isbn, title, author, total_copies=1):
        self.isbn = self._normalize_isbn(isbn)
        self.title = self._validate_title(title)
        self.author = author
        if total_copies < 0:
            raise ValueError("Total copies cannot be negative")
        self.total_copies = total_copies
        self.available_copies = total_copies

    @staticmethod
    def _normalize_isbn(isbn):
        digits = isbn.replace("-", "")
        if not (digits.isdigit() and len(digits) in VALID_ISBN_LENGTHS):
            raise ValueError("ISBN must have 10 or 13 digits")
        return digits

    @staticmethod
    def _validate_title(title):
        if not title.strip():
            raise ValueError("Title is required")
        return title

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if not self.is_available():
            raise BookNotAvailableError(f"No copies of {self.isbn} are available")
        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies >= self.total_copies:
            raise InvalidReturnError(f"Every copy of {self.isbn} is already on the shelf")
        self.available_copies += 1
