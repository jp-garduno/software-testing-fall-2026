"""Book: a title in the catalog and how many of its copies are on the shelf."""

from . import errors

VALID_ISBN_LENGTHS = (10, 13)


class Book:
    """A catalog entry whose copies can be lent out."""

    def __init__(self, isbn, title, author, copies=1):
        self._validate_isbn(isbn)
        self._validate_title(title)
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

    @staticmethod
    def _validate_isbn(isbn):
        """Accept only an ISBN-10 or ISBN-13 written as plain digits."""
        if len(isbn) not in VALID_ISBN_LENGTHS or not isbn.isdigit():
            raise ValueError("ISBN must have 10 or 13 digits")

    @staticmethod
    def _validate_title(title):
        """Reject a missing or blank title."""
        if not title or not title.strip():
            raise ValueError("Title is required")

    def is_available(self):
        """Return True while at least one copy is on the shelf."""
        return self.available_copies > 0

    def borrow(self):
        """Take one copy off the shelf."""
        if not self.is_available():
            raise errors.BookNotAvailableError(f"No copies of '{self.title}' are available")
        self.available_copies -= 1

    def return_copy(self):
        """Put one borrowed copy back on the shelf."""
        if self.available_copies == self.total_copies:
            raise errors.InvalidReturnError(f"Every copy of '{self.title}' is already on the shelf")
        self.available_copies += 1
