"""Book domain model."""


class Book:
    """Book behavior developed test first."""

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
