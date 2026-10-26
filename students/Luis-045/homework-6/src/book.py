"""Book inventory and availability."""


class Book:
    """A catalog entry with its inventory."""

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
