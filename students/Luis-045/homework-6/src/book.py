"""Book inventory and availability."""


class Book:
    """A catalog entry with its inventory."""

    def __init__(self, isbn, title, author, total_copies=1, **metadata):
        self._validate_isbn(isbn)
        self.isbn = isbn
        if not title.strip():
            raise ValueError("Book title is required")
        self.title = title
        self.author = author
        self.metadata = metadata
        if (
            not isinstance(total_copies, int)
            or isinstance(total_copies, bool)
            or total_copies < 0
        ):
            raise ValueError("Total copies must be nonnegative")
        self.total_copies = total_copies
        self.available_copies = total_copies

    @staticmethod
    def _validate_isbn(isbn):
        """Reject ISBNs outside the assignment's digit format."""
        if (
            not isinstance(isbn, str)
            or len(isbn) not in (10, 13)
            or not isbn.isascii()
            or not isbn.isdigit()
        ):
            raise ValueError("ISBN must contain 10 or 13 digits")

    def is_available(self):
        """Whether at least one copy can be borrowed."""
        return self.available_copies > 0

    def borrow(self):
        """Lend one available copy."""
        if not self.is_available():
            raise ValueError("No copies available")
        self.available_copies -= 1

    def return_copy(self):
        """Restore one previously borrowed copy."""
        if self.available_copies == self.total_copies:
            raise ValueError("No borrowed copies to return")
        self.available_copies += 1
