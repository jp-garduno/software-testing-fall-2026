class Book:
    def __init__(self, isbn, title, author, total_copies=1):
        if len(isbn) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 digits")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self):
        return self.available_copies > 0