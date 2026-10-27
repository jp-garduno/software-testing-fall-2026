class Book:
    def __init__(self, isbn, title, author, copies=1):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.available_copies = copies

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if not self.is_available():
            raise ValueError("No copies available")
        self.available_copies -= 1

    def return_copy(self):
        self.available_copies += 1
