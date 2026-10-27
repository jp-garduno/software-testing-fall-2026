"""Book: a title in the catalog and how many of its copies are on the shelf."""


class Book:
    """A catalog entry whose copies can be lent out."""

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
