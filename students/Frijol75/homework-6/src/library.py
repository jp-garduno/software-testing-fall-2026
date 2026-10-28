"""Library core coordinator for books, members, and operations."""
from datetime import date
from typing import Any, Dict, List, Optional
import uuid

from src.book import Book
from src.member import Member
from src.loan import LoanRecord, calculate_late_fee
from src.reservation import Reservation, ReservationManager


class Library:
    """Manages the catalog, members, and loans of the library."""

    def __init__(self) -> None:
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.loans: List[LoanRecord] = []
        self.reservations = ReservationManager()

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

    def borrow_book(
        self,
        member_id: str,
        isbn: str,
        borrow_date: Optional[date] = None,
    ) -> bool:
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

        b_date = borrow_date or date.today()
        loan = LoanRecord(
            loan_id=str(uuid.uuid4()),
            member_id=member_id,
            isbn=isbn,
            borrow_date=b_date,
        )
        self.loans.append(loan)
        return True

    def return_book(
        self,
        member_id: str,
        isbn: str,
        return_date: Optional[date] = None,
    ) -> bool:
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

        r_date = return_date or date.today()
        for loan in reversed(self.loans):
            if loan.member_id == member_id and loan.isbn == isbn and loan.return_date is None:
                loan.return_date = r_date
                break

        self.reservations.notify_next(isbn)
        return True

    def reserve_book(self, member_id: str, isbn: str) -> Dict[str, Any]:
        """Reserve an unavailable book for a registered member."""
        if member_id not in self.members:
            raise KeyError("Member not registered")
        if isbn not in self.books:
            raise KeyError("Book not found in catalog")

        member = self.members[member_id]
        book = self.books[isbn]

        if book.is_available():
            raise ValueError("Cannot reserve a book with available copies")
        if isbn in member.borrowed_books:
            raise ValueError("Member currently holds a copy of this book")
        if self.reservations.is_member_in_queue(member_id, isbn):
            raise ValueError("Book is already reserved by this member")

        res = Reservation(
            reservation_id=str(uuid.uuid4()),
            member_id=member_id,
            isbn=isbn,
        )
        self.reservations.add_reservation(res)
        return {"status": res.status, "member_id": res.member_id, "isbn": res.isbn}

    def cancel_reservation(self, member_id: str, isbn: str) -> bool:
        """Cancel a pending reservation."""
        return self.reservations.cancel_reservation(member_id, isbn)

    def get_book_reservations(self, isbn: str) -> List[str]:
        """Get list of member IDs queued for the book."""
        return self.reservations.get_queue(isbn)

    def get_next_reservation_notification(self, isbn: str) -> Optional[str]:
        """Get the last member notified when the book became available."""
        return self.reservations.get_latest_notified(isbn)

    def search_by_title(self, title: str) -> List[Book]:
        """Search books by title substring (case-insensitive)."""
        if not isinstance(title, str):
            raise TypeError("Search query must be a string")
        query = title.strip().lower()
        return [b for b in self.books.values() if query in b.title.lower()]

    def search_by_author(self, author: str) -> List[Book]:
        """Search books by author substring (case-insensitive)."""
        if not isinstance(author, str):
            raise TypeError("Search query must be a string")
        query = author.strip().lower()
        return [b for b in self.books.values() if query in b.author.lower()]

    def get_available_books(self) -> List[Book]:
        """Return a list of books that have at least one copy available."""
        return [b for b in self.books.values() if b.is_available()]

    def filter_books(
        self,
        genre: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        min_rating: Optional[float] = None,
        sort_by: Optional[str] = None,
        reverse: bool = False,
    ) -> List[Book]:
        """Filter books using combined AND criteria and optional sorting."""
        results = list(self.books.values())

        if genre is not None:
            g = genre.strip().lower()
            results = [b for b in results if b.genre and g in b.genre.lower()]

        if year_from is not None:
            results = [b for b in results if b.year is not None and b.year >= year_from]

        if year_to is not None:
            results = [b for b in results if b.year is not None and b.year <= year_to]

        if min_rating is not None:
            results = [b for b in results if b.rating is not None and b.rating >= min_rating]

        if sort_by:
            key_map = {
                "title": lambda b: b.title.lower(),
                "year": lambda b: b.year if b.year is not None else 0,
                "rating": lambda b: b.rating if b.rating is not None else 0.0,
            }
            if sort_by in key_map:
                results.sort(key=key_map[sort_by], reverse=reverse)

        return results

    def calculate_member_late_fees(
        self,
        member_id: str,
        as_of_date: Optional[date] = None,
    ) -> float:
        """Calculate total late fees for all loans of a given member."""
        if member_id not in self.members:
            raise KeyError("Member not registered")
        check_date = as_of_date or date.today()
        total_fee = 0.0
        for loan in self.loans:
            if loan.member_id == member_id:
                total_fee += calculate_late_fee(loan, return_date=loan.return_date or check_date)
        return total_fee
