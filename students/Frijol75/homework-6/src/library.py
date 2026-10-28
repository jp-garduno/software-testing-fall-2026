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

    def borrow_book(self, member_id: str, isbn: str) -> bool:
        """Borrow a book for a registered member."""
        if member_id not in self.members:
            raise KeyError("Member not registered")
        if isbn not in self.books:
            raise KeyError("Book not found in catalog")

        member = self.members[member_id]
        book = self.books[isbn]

        if not book.is_available():
            raise ValueError("Book is not currently available")
        if not member.can_borrow():
            raise ValueError("Borrow limit reached")

        book.borrow()
        member.add_borrowed_book(isbn)
        return True

    def return_book(self, member_id: str, isbn: str) -> bool:
        """Return a borrowed book by a registered member."""
        if member_id not in self.members:
            raise KeyError("Member not registered")
        if isbn not in self.books:
            raise KeyError("Book not found in catalog")

        member = self.members[member_id]
        book = self.books[isbn]

        if isbn not in member.borrowed_books:
            raise ValueError("Book not borrowed by this member")

        book.return_copy()
        member.return_book(isbn)
        return True
