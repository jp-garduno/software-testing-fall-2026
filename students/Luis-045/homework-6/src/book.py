"""Book inventory and availability."""


class Book:
    """A catalog entry with its inventory."""

    def __init__(self, isbn, title, author, total_copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
