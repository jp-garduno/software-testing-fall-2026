class Book:
    def __init__(self, isbn, title, author, copies=1):
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 digits")
        self.title = title
        self.isbn = isbn
        self.author = author
        self.available_copies = copies
        self.total_copies = copies

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if not self.is_available():
            raise ValueError("No copies available")
        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies >= self.total_copies:
            raise ValueError("All copies already returned")
        self.available_copies += 1
