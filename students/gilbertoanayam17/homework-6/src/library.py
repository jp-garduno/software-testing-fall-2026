"""Library: the catalog, its members, and the loans between them."""

from datetime import date

from . import errors
from .loan import Loan

class Library:
    """Coordinates books and members so every loan follows the library's rules."""

    def __init__(self, clock=date.today):
        self._books = {}
        self._members = {}
        self._loans = []
        self._fees_owed = {}
        self._clock = clock

    def add_book(self, book):
        """Add a book to the catalog, indexed by its ISBN."""
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for this ISBN."""
        if isbn not in self._books:
            raise errors.BookNotFoundError(f"No book with ISBN {isbn}")

        return self._books[isbn]

    def register_member(self, member):
        """Register a member, indexed by their id."""
        self._members[member.member_id] = member

    def get_member(self, member_id):
        """Return the registered member with this id."""
        if member_id not in self._members:
            raise errors.MemberNotFoundError(f"No member with id {member_id}")

        return self._members[member_id]

    def borrow_book(self, member_id, isbn):
        """Lend one copy of a book to a member."""
        member = self.get_member(member_id)
        member.ensure_can_borrow()
        self.get_book(isbn).borrow()
        member.add_borrowed_book(isbn)
        self._loans.append(Loan(member_id, isbn, self._clock(), member.category.daily_late_fee))

    def return_book(self, member_id, isbn):
        """Take back a member's copy of a book."""
        self.get_member(member_id).return_book(isbn)
        self.get_book(isbn).return_copy()
        loan = self._close_loan(member_id, isbn)
        self._fees_owed[member_id] = self._fees_owed.get(member_id, 0) + loan.late_fee(self._clock())

    def search_by_title(self, title):
        """Return the books whose title contains `title`, ignoring case."""
        return self._search("title", title)

    def search_by_author(self, author):
        """Return the books whose author contains `author`, ignoring case."""
        return self._search("author", author)

    def _search(self, field, text):
        """Return the books whose `field` contains `text`, ignoring case."""
        needle = text.lower()
        return [book for book in self._books.values() if needle in getattr(book, field).lower()]

    def get_available_books(self):
        """Return the books with at least one copy on the shelf."""
        return [book for book in self._books.values() if book.is_available()]

    def calculate_late_fees(self, member_id):
        """Return the late fees a member owes."""
        today = self._clock()
        accruing = sum(loan.late_fee(today) for loan in self._loans if loan.member_id == member_id)
        return self._fees_owed.get(member_id, 0) + accruing

    def _close_loan(self, member_id, isbn):
        """Remove the member's open loan of this book and return it."""
        loan = next(loan for loan in self._loans if (loan.member_id, loan.isbn) == (member_id, isbn))
        self._loans.remove(loan)
        return loan
