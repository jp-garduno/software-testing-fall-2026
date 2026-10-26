"""Book model for Library Management System."""


class Book:
    """Represents a book in the library catalog."""

    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        total_copies: int = 1,
    ) -> None:
        self.isbn = str(isbn).strip()
        self.title = str(title).strip()
        self.author = str(author).strip()
        self.total_copies = int(total_copies)
        self.available_copies = self.total_copies
