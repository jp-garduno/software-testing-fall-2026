"""Library management system core service."""
from typing import Dict
from src.book import Book
from src.member import Member


class Library:
    """Manages catalog, members, and borrowing operations."""

    def __init__(self) -> None:
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}

    def add_book(self, book: Book) -> None:
        """Add a new book to the library catalog."""
        if book.isbn in self.books:
            raise ValueError("Book already exists in catalog")
        self.books[book.isbn] = book

    def get_book(self, isbn: str) -> Book:
        """Retrieve a book from catalog by its ISBN."""
        cleaned_isbn = str(isbn).strip()
        if cleaned_isbn not in self.books:
            raise KeyError("Book not found in catalog")
        return self.books[cleaned_isbn]
