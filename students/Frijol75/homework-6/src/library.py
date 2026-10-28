"""Library core coordinator for books, members, and operations."""
from typing import Dict, List, Optional
from src.book import Book
from src.member import Member


class Library:
    """Manages the catalog, members, and loans of the library."""

    def __init__(self) -> None:
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}

    def add_book(self, book: Book) -> None:
        """Add a book to the library catalog."""
        if not isinstance(book, Book):
            raise TypeError("Expected Book instance")
        if book.isbn in self.books:
            existing = self.books[book.isbn]
            existing.total_copies += book.total_copies
            existing.available_copies += book.total_copies
        else:
            self.books[book.isbn] = book

    def register_member(self, member: Member) -> None:
        """Register a new member in the library system."""
        if not isinstance(member, Member):
            raise TypeError("Expected Member instance")
        if member.member_id in self.members:
            raise ValueError("Member with this ID already registered")
        self.members[member.member_id] = member
