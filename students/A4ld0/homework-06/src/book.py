"""Books and copy availability."""


class Book:
    def __init__(self, isbn, title, author, total_copies=1):
        if not isinstance(isbn, str) or not isbn.isascii() or not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValueError("ISBN must have 10 or 13 digits")
        self.isbn = isbn
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Book title is required")
        self.title = title
        self.author = author
        if type(total_copies) is not int or total_copies < 0:
            raise ValueError("Total copies must be a nonnegative integer")
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if not self.is_available():
            raise ValueError("No available copies")
        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies == self.total_copies:
            raise ValueError("No borrowed copy to return")
        self.available_copies += 1
