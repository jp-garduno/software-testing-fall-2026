"""Book: a title in the catalog and how many of its copies are on the shelf."""

from . import errors


class Book:
    """A catalog entry whose copies can be lent out."""

    def __init__(self, isbn, title, author, copies=1):
        if len(isbn) not in (10, 13) or not isbn.isdigit():
            raise ValueError("ISBN must have 10 or 13 digits")

        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

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
