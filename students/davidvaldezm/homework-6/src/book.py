"""Book domain model."""


class Book:
    """Book behavior developed test first."""

    def __init__(self, isbn, title, author, copies=1):
        valid_isbn = (
            isinstance(isbn, str)
            and len(isbn) in (10, 13)
            and isbn.isascii()
            and isbn.isdigit()
        )
        if not valid_isbn:
            raise ValueError("ISBN must contain 10 or 13 ASCII digits")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Book title is required")
        if not isinstance(copies, int) or isinstance(copies, bool) or copies < 0:
            raise ValueError("copies must be a nonnegative integer")
        self.total_copies = copies
        self.available_copies = copies
        self.isbn = isbn
        self.title = title
        self.author = author

    def is_available(self):
        """Return whether at least one copy can be borrowed."""
        return self.available_copies > 0

    def borrow(self):
        """Borrow one copy or raise ValueError when stock is exhausted."""
        if not self.is_available():
            raise ValueError("No copies available")
        self.available_copies -= 1

    def return_copy(self):
        """Restore one borrowed copy without exceeding owned stock."""
        if self.available_copies == self.total_copies:
            raise ValueError("All copies already returned")
        self.available_copies += 1
