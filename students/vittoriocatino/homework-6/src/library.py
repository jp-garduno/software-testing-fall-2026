"""Library catalog and borrowing workflows."""

from book import Book
from member import Member


class Library:
    """In-memory library coordinating books and members."""

    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.borrowing_history: list[dict] = []
        self.reservations: dict[str, list[str]] = {}

    def add_book(self, book: Book) -> None:
        if book.isbn in self.books:
            raise ValueError("book ISBN already exists")
        self.books[book.isbn] = book

    def register_member(self, member: Member) -> None:
        if member.member_id in self.members:
            raise ValueError("member ID already exists")
        self.members[member.member_id] = member
