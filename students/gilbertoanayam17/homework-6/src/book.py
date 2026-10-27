"""Book: a title in the catalog and how many of its copies are on the shelf."""


class Book:
    """A catalog entry whose copies can be lent out."""

    def __init__(self, isbn, title, author, copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available_copies = copies

    def is_available(self):
        """Return True while at least one copy is on the shelf."""
        return self.available_copies > 0

    def borrow(self):
        """Take one copy off the shelf."""
        self.available_copies -= 1
