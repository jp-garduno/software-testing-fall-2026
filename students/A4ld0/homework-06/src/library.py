"""Catalog and lending operations."""
from datetime import date, timedelta


class Library:
    def __init__(self):
        self.catalog = {}
        self.members = {}
        self.loans = []

    def add_book(self, book):
        if book.isbn in self.catalog:
            raise ValueError("ISBN already registered")
        self.catalog[book.isbn] = book

    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError("Duplicate member ID")
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn, borrowed_on=None):
        member = self._get_member(member_id)
        book = self._get_book(isbn)
        if not member.can_borrow():
            raise ValueError("Member borrowing limit reached")
        book.borrow()
        member.add_borrowed_book(isbn)
        borrowed_on = borrowed_on or date.today()
        self.loans.append(dict(member_id=member_id, isbn=isbn,
                               borrowed_on=borrowed_on,
                               due_on=borrowed_on + timedelta(days=14)))

    def _get_member(self, member_id):
        if member_id not in self.members:
            raise ValueError("Unknown member")
        return self.members[member_id]

    def _get_book(self, isbn):
        if isbn not in self.catalog:
            raise ValueError("Unknown ISBN")
        return self.catalog[isbn]

    def return_book(self, member_id, isbn, returned_on=None):
        member = self._get_member(member_id)
        book = self._get_book(isbn)
        member.return_book(isbn)
        book.return_copy()
        loan = next(loan for loan in self.loans
                    if loan["member_id"] == member_id and loan["isbn"] == isbn
                    and loan.get("returned_on") is None)
        loan["returned_on"] = returned_on or date.today()

    def search_by_title(self, title):
        return [book for book in self.catalog.values()
                if title.casefold() in book.title.casefold()]

    def search_by_author(self, author):
        return [book for book in self.catalog.values()
                if author.casefold() in book.author.casefold()]

    def get_available_books(self):
        return [book for book in self.catalog.values() if book.is_available()]

    def calculate_late_fees(self, member_id, as_of=None):
        as_of = as_of or date.today()
        return sum(self._loan_fee(loan, as_of)
                   for loan in self.loans if loan["member_id"] == member_id)

    @staticmethod
    def _loan_fee(loan, as_of):
        end = min(as_of, loan.get("returned_on") or as_of)
        return max(0, (end - loan["due_on"]).days)
