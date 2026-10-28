"""Book domain model."""


class Book:
    """Book behavior developed test first."""

    def __init__(self, isbn, title, author, copies=1):
        self.total_copies = copies
        self.available_copies = copies
        self.isbn = isbn
        self.title = title
        self.author = author
