"""Books and copy availability."""


class Book:
    def __init__(self, isbn, title, author, total_copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
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
