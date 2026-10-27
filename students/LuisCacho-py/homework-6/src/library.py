"""Library management system core service."""
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
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
        self.member_balances: Dict[str, float] = {}

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

    def return_book(
        self,
        member_id: str,
        isbn: str,
        return_date: Optional[date] = None,
    ) -> float:
        """Return a borrowed book to the library and compute late fees."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)

        if book.isbn not in member.borrowed_books:
            raise ValueError("Book was not borrowed by this member")

        member.return_book(book.isbn)
        book.return_copy()

        # Find matching active loan
        loan: Optional[Loan] = None
        for active in self.active_loans:
            if active.member_id == member.member_id and active.isbn == book.isbn:
                loan = active
                break

        actual_return = return_date or date.today()
        fee = 0.0

        if loan is not None:
            self.active_loans.remove(loan)
            loan.return_date = actual_return
            if actual_return > loan.due_date:
                days_overdue = (actual_return - loan.due_date).days
                fee = float(days_overdue * 1.0)
            loan.late_fee = fee
            self.loan_history.append(loan)
            if fee > 0.0:
                self.member_balances[member.member_id] = (
                    self.member_balances.get(member.member_id, 0.0) + fee
                )

        return fee

    def search_by_title(self, title: str) -> List[Book]:
        """Search books by title substring, case-insensitively."""
        term = str(title).strip().lower()
        if not term:
            return []
        return [b for b in self.books.values() if term in b.title.lower()]

    def search_by_author(self, author: str) -> List[Book]:
        """Search books by author substring, case-insensitively."""
        term = str(author).strip().lower()
        if not term:
            return []
        return [b for b in self.books.values() if term in b.author.lower()]

    def get_available_books(self) -> List[Book]:
        """Return list of books currently having at least one available copy."""
        return [b for b in self.books.values() if b.is_available()]

    def get_member_total_late_fees(
        self,
        member_id: str,
        as_of: Optional[date] = None,
    ) -> float:
        """Calculate total late fees owed by member (past unpaid + active overdue)."""
        member = self.get_member(member_id)
        current = as_of or date.today()
        total = self.member_balances.get(member.member_id, 0.0)

        for loan in self.active_loans:
            if loan.member_id == member.member_id and current > loan.due_date:
                days_overdue = (current - loan.due_date).days
                total += float(days_overdue * 1.0)

        return round(total, 2)

    def pay_late_fee(self, member_id: str, amount: float) -> float:
        """Pay late fees for a member and return the remaining fee balance."""
        member = self.get_member(member_id)
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        current_balance = self.member_balances.get(member.member_id, 0.0)
        if amount > current_balance:
            raise ValueError("Payment exceeds outstanding balance")

        self.member_balances[member.member_id] = round(current_balance - amount, 2)
        return self.member_balances[member.member_id]

    def get_member_history(self, member_id: str) -> List[Loan]:
        """Retrieve all active and returned loans for a given member."""
        member = self.get_member(member_id)
        active = [loan for loan in self.active_loans if loan.member_id == member.member_id]
        past = [loan for loan in self.loan_history if loan.member_id == member.member_id]
        return active + past

    def get_most_borrowed_books(self, top_n: int = 5) -> List[Tuple[Book, int]]:
        """Calculate and return the top most borrowed books."""
        counts: Dict[str, int] = {}
        for loan in self.active_loans + self.loan_history:
            counts[loan.isbn] = counts.get(loan.isbn, 0) + 1

        sorted_items = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        results: List[Tuple[Book, int]] = []
        for isbn, count in sorted_items[:top_n]:
            if isbn in self.books:
                results.append((self.books[isbn], count))
        return results
