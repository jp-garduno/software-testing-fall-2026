"""Library management system core service."""
from datetime import date, timedelta
from typing import Dict, List, Optional
from src.book import Book
from src.member import Member


class Loan:
    """Represents an active or historic book loan."""

    def __init__(
        self,
        member_id: str,
        isbn: str,
        borrow_date: Optional[date] = None,
        due_date: Optional[date] = None,
    ) -> None:
        self.member_id = member_id
        self.isbn = isbn
        self.borrow_date = borrow_date or date.today()
        self.due_date = due_date or (self.borrow_date + timedelta(days=14))
        self.return_date: Optional[date] = None
        self.late_fee: float = 0.0


class Library:
    """Manages catalog, members, and borrowing operations."""

    def __init__(self) -> None:
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.active_loans: List[Loan] = []
        self.loan_history: List[Loan] = []

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

    def register_member(self, member: Member) -> None:
        """Register a member in the library system."""
        if member.member_id in self.members:
            raise ValueError("Member already registered")
        self.members[member.member_id] = member

    def get_member(self, member_id: str) -> Member:
        """Retrieve a registered member by member ID."""
        cleaned_id = str(member_id).strip()
        if cleaned_id not in self.members:
            raise KeyError("Member not found in library")
        return self.members[cleaned_id]

    def borrow_book(
        self,
        member_id: str,
        isbn: str,
        borrow_date: Optional[date] = None,
    ) -> Loan:
        """Borrow a book for a registered member."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)

        if not member.can_borrow():
            raise ValueError("Borrow limit reached")
        if not book.is_available():
            raise RuntimeError("No copies available for borrowing")

        book.borrow()
        member.add_borrowed_book(isbn)

        loan = Loan(
            member_id=member.member_id,
            isbn=book.isbn,
            borrow_date=borrow_date,
        )
        self.active_loans.append(loan)
        return loan
