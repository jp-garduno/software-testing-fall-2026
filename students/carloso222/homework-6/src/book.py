"""Book entity: a title in the catalog with a number of physical copies."""


class Book:
    """A catalog entry that tracks how many of its copies are on the shelf."""

    def __init__(self, isbn, title, author, total_copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
