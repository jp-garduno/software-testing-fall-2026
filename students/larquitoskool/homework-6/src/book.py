class Book:
    def __init__(self, isbn, title, author, total_copies=1):
        if len(isbn) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 digits")
        if not title:
            raise ValueError("Title is required")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if not self.is_available():
            raise ValueError("Book is not available")
        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies >= self.total_copies:
            raise ValueError("All copies returned")
        self.available_copies += 1