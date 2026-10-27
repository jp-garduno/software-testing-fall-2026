class Book:
    VALID_ISBN_LENGTHS = (10, 13)
    def __init__(self, isbn, title, author, copies=1):
        self._validate_isbn(isbn)
        if not title or not title.strip():
            raise ValueError("Title is required")

        self.title = title
        self.isbn = isbn
        self.author = author
        self.available_copies = copies
        self.total_copies = copies

    @classmethod
    def _validate_isbn(cls, isbn):
        if not isbn.isdigit() or len(isbn) not in cls.VALID_ISBN_LENGTHS:
            raise ValueError("ISBN must be 10 or 13 digits")

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
