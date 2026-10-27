ISBN_LENGTHS = (10, 13)


class Book:
    def __init__(self, isbn, title, author, total_copies=1):
        if len(isbn) not in ISBN_LENGTHS or not isbn.isdigit():
            raise ValueError("ISBN must be 10 or 13 digits")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if not self.is_available():
            raise ValueError(f"No copies available for '{self.title}'")
        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies == self.total_copies:
            raise ValueError(f"All copies of '{self.title}' are already in")
        self.available_copies += 1
