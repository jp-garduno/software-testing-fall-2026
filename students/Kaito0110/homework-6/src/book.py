"""Book model for the Library Management System."""


class Book:
    """Represents a book in the library catalog."""

    # pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        isbn,
        title,
        author,
        total_copies=1,
        available_copies=None,
        genre=None,
        publication_year=None,
        rating=None,
    ):
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValueError("ISBN must contain 10 or 13 digits")

        if not title or not title.strip():
            raise ValueError("Book title cannot be empty")

        if total_copies < 0:
            raise ValueError("Total copies cannot be negative")

        if available_copies is None:
            available_copies = total_copies

        if available_copies < 0:
            raise ValueError("Available copies cannot be negative")

        if available_copies > total_copies:
            raise ValueError("Available copies cannot exceed total copies")

        if rating is not None and not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5")

        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.genre = genre
        self.publication_year = publication_year
        self.rating = rating

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
