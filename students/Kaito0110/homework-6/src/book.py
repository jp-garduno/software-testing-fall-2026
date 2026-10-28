"""Book model for the Library Management System."""


class Book:
    """Represents a book in the library catalog."""

    def __init__(self, isbn, title, author, total_copies=1, available_copies=1):
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValueError("ISBN must contain 10 or 13 digits")

        if not title or not title.strip():
            raise ValueError("Book title cannot be empty")

        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = available_copies

    def is_available(self):
        """Return True if at least one copy is available to borrow."""
        return self.available_copies > 0

    def borrow(self):
        """Decrement available copies by 1 or raise ValueError if unavailable."""
        if self.available_copies > 0:
            self.available_copies -= 1
        else:
            raise ValueError("No copies available")

    def return_copy(self):
        """Increment available copies up to total_copies."""
        if self.available_copies < self.total_copies:
            self.available_copies += 1
