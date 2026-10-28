"""Book domain entity."""


class Book:
    """A catalog book with identifying metadata and copies."""

    def __init__(self, isbn: str, title: str, author: str, copies: int = 1) -> None:
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies
