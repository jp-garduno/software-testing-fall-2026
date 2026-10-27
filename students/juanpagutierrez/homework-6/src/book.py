"""Book entity of the library catalog."""


class Book:
    """A title in the catalog, with one or more physical copies."""

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
