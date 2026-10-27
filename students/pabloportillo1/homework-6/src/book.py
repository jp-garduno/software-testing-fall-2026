ISBN_LENGTHS = (10, 13)


class Book:
    def __init__(self, isbn, title, author, total_copies=1):
        self._validate(isbn, title, total_copies)
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def is_available(self):
        return self.available_copies > 0

    def ensure_available(self):
        if not self.is_available():
            raise ValueError(f"No copies available for '{self.title}'")

    def borrow(self):
        self.ensure_available()
        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies == self.total_copies:
            raise ValueError(f"All copies of '{self.title}' are already in")
        self.available_copies += 1

    @staticmethod
    def _validate(isbn, title, total_copies):
        if len(isbn) not in ISBN_LENGTHS or not isbn.isdigit():
            raise ValueError("ISBN must be 10 or 13 digits")
        if not title.strip():
            raise ValueError("Title is required")
        if total_copies < 0:
            raise ValueError("Total copies cannot be negative")
