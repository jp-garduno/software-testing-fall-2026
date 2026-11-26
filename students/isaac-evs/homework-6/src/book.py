class Book:
    def __init__(self, isbn, title, author, copies=1):
        self._validate_isbn(isbn)
        self._validate_title(title)
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

    @staticmethod
    def _validate_isbn(isbn):
        if len(isbn) not in (10, 13) or not isbn.isdigit():
            raise ValueError("ISBN must be 10 or 13 digits")

    @staticmethod
    def _validate_title(title):
        if not title or not title.strip():
            raise ValueError("Title is required")

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if not self.is_available():
            raise ValueError("No copies available")
        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies >= self.total_copies:
            raise ValueError("All copies are already returned")
        self.available_copies += 1
