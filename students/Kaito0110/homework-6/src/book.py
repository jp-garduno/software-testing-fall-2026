"""Book model for the Library Management System."""


class Book:
    """Represents a book in the library catalog."""

    def __init__(self, isbn, title, author, total_copies=1, available_copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = available_copies

    def is_available(self):
        """Return True if at least one copy is available to borrow."""
        return self.available_copies > 0
