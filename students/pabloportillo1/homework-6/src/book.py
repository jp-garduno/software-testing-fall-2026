from dataclasses import dataclass

ISBN_LENGTHS = (10, 13)


@dataclass(frozen=True)
class BookDetails:
    genre: str | None = None
    year: int | None = None
    rating: float | None = None

    def __post_init__(self):
        if self.rating is not None and not 0 <= self.rating <= 5:
            raise ValueError("Rating must be between 0 and 5")


class Book:
    def __init__(self, isbn, title, author, total_copies=1, *, details=None):  # pylint: disable=too-many-arguments
        self._validate(isbn, title, total_copies)
        self.details = details or BookDetails()
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
