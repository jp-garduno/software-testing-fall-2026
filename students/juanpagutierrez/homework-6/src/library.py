"""Library facade: catalog, members and lending rules."""

from datetime import date
from decimal import Decimal

from src.exceptions import BookNotFoundError, BorrowLimitExceededError, MemberNotFoundError
from src.late_fees import calculate_late_fee, due_date_for
from src.loan import Loan


class Library:
    """Coordinates books and members."""

    def __init__(self, clock=date.today):
        self._clock = clock
        self._books = {}
        self._members = {}
        self._loans = []

    def add_book(self, book):
        """Add ``book`` to the catalog."""
        if book.isbn in self._books:
            raise ValueError(f"A book with ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for ``isbn``."""
        if isbn not in self._books:
            raise BookNotFoundError(f"No book with ISBN {isbn}")
        return self._books[isbn]

    def register_member(self, member):
        """Register ``member`` so they can borrow books."""
        if member.member_id in self._members:
            raise ValueError(f"Member {member.member_id} is already registered")
        self._members[member.member_id] = member

    def get_member(self, member_id):
        """Return the registered member with ``member_id``."""
        if member_id not in self._members:
            raise MemberNotFoundError(f"No member with id {member_id}")
        return self._members[member_id]

    def borrow_book(self, member_id, isbn):
        """Lend one copy of ``isbn`` to ``member_id``."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        if not member.can_borrow():
            raise BorrowLimitExceededError(f"{member_id} reached the limit of {member.max_borrow_limit}")
        book.borrow()
        member.add_borrowed_book(isbn)
        today = self._clock()
        self._loans.append(Loan(member_id, isbn, today, due_date_for(today)))

    def get_loans(self, member_id):
        """Return every loan made to ``member_id``, oldest first."""
        return [loan for loan in self._loans if loan.member_id == member_id]

    def return_book(self, member_id, isbn):
        """Take back the copy of ``isbn`` lent to ``member_id``."""
        self.get_member(member_id).return_book(isbn)
        self.get_book(isbn).return_copy()
        open_loan = next(loan for loan in self._loans
                         if loan.member_id == member_id and loan.isbn == isbn and loan.returned_on is None)
        open_loan.returned_on = self._clock()

    def search_by_title(self, title):
        """Return books whose title contains ``title`` (case-insensitive)."""
        return self._search(title, lambda book: book.title)

    def search_by_author(self, author):
        """Return books whose author contains ``author`` (case-insensitive)."""
        return self._search(author, lambda book: book.author)

    def _search(self, text, field):
        needle = text.lower()
        return [book for book in self._books.values() if needle in field(book).lower()]

    def get_available_books(self):
        """Return every book with at least one copy on the shelf."""
        return [book for book in self._books.values() if book.is_available()]

    def calculate_member_fees(self, member_id):
        """Total late fees ``member_id`` owes as of today."""
        today = self._clock()
        return sum((calculate_late_fee(loan.due_date, loan.returned_on or today) for loan in self.get_loans(member_id)), Decimal("0"))
