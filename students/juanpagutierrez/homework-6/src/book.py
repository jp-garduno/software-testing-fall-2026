"""Book entity of the library catalog."""


class Book:
    """A title in the catalog, with one or more physical copies."""

    def __init__(self, isbn, title, author, total_copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
