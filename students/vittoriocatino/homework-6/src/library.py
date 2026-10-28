"""Library catalog and borrowing workflows."""

from datetime import date, timedelta
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

    def _member_and_book(self, member_id: str, isbn: str) -> tuple[Member, Book]:
        if member_id not in self.members:
            raise ValueError("member not found")
        if isbn not in self.books:
            raise ValueError("book not found")
        return self.members[member_id], self.books[isbn]

    def borrow_book(self, member_id: str, isbn: str) -> None:
        member, book = self._member_and_book(member_id, isbn)
        book.borrow()
        try:
            member.add_borrowed_book(isbn)
        except ValueError:
            book.return_copy()
            raise
        self.borrowing_history.append(
            {
                "member_id": member_id,
                "isbn": isbn,
                "returned": False,
                "due_date": date.today() + timedelta(days=14),
            }
        )

    def return_book(self, member_id: str, isbn: str) -> None:
        member, book = self._member_and_book(member_id, isbn)
        member.return_book(isbn)
        book.return_copy()
        next(item for item in reversed(self.borrowing_history) if item["member_id"] == member_id and item["isbn"] == isbn and not item["returned"])["returned"] = True

    def search_by_title(self, title: str) -> list[Book]:
        return [book for book in self.books.values() if title.lower() in book.title.lower()]

    def search_by_author(self, author: str) -> list[Book]:
        return [book for book in self.books.values() if author.lower() in book.author.lower()]

    def get_available_books(self) -> list[Book]:
        return [book for book in self.books.values() if book.is_available()]

    def calculate_late_fees(self, member_id: str, today: date | None = None) -> int:
        """Charge one dollar for each overdue day of an active loan."""
        if member_id not in self.members:
            raise ValueError("member not found")
        current_date = today or date.today()
        return sum(
            max(0, (current_date - item["due_date"]).days)
            for item in self.borrowing_history
            if item["member_id"] == member_id and not item["returned"]
        )

    def reserve_book(self, member_id: str, isbn: str) -> None:
        """Add a member to an unavailable book's first-in-first-out queue."""
        member, book = self._member_and_book(member_id, isbn)
        del member
        if book.is_available():
            raise ValueError("available books cannot be reserved")
        queue = self.reservations.setdefault(isbn, [])
        if member_id in queue:
            raise ValueError("member already has a reservation")
        queue.append(member_id)
