"""Books and copy availability."""
from dataclasses import dataclass


@dataclass
class SearchMetadata:
    """Optional attributes used together by catalog filters."""
    genre: str | None = None
    publication_year: int | None = None
    rating: float | None = None


class Book:
    def __init__(self, isbn, title, author, total_copies=1, **metadata):
        valid_isbn = (
            isinstance(isbn, str) and isbn.isascii()
            and isbn.isdigit() and len(isbn) in (10, 13)
        )
        if not valid_isbn:
            raise ValueError("ISBN must have 10 or 13 digits")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Book title is required")
        if (not isinstance(total_copies, int) or isinstance(total_copies, bool)
                or total_copies < 0):
            raise ValueError("Total copies must be a nonnegative integer")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
        self._metadata = SearchMetadata(**metadata)

    @property
    def genre(self):
        return self._metadata.genre

    @genre.setter
    def genre(self, value):
        self._metadata.genre = value

    @property
    def publication_year(self):
        return self._metadata.publication_year

    @publication_year.setter
    def publication_year(self, value):
        self._metadata.publication_year = value

    @property
    def rating(self):
        return self._metadata.rating

    @rating.setter
    def rating(self, value):
        self._metadata.rating = value

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
