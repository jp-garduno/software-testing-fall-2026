"""Book domain model."""


class Book:
    """Book behavior developed test first."""

    def __init__(self, isbn, title, author, copies=1):
        if not isinstance(isbn, str) or len(isbn) not in (10, 13) or not isbn.isascii() or not isbn.isdigit():
            raise ValueError('ISBN must contain 10 or 13 ASCII digits')
        if not isinstance(title, str) or not title.strip():
            raise ValueError('Book title is required')
        if type(copies) is not int or copies < 0:
            raise ValueError('copies must be a nonnegative integer')
        self.total_copies = copies
        self.available_copies = copies
        self.isbn = isbn
        self.title = title
        self.author = author
