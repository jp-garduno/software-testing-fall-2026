"""Catalog and lending operations."""
from datetime import date, timedelta
from collections import Counter


class Library:
    LOAN_PERIOD_DAYS = 14
    DAILY_LATE_FEE = 1

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
        borrowed_on = self._resolve_date(borrowed_on, "Borrowing")
        book.borrow()
        member.add_borrowed_book(isbn)
        self.loans.append(dict(member_id=member_id, isbn=isbn,
                               borrowed_on=borrowed_on,
                               due_on=borrowed_on + timedelta(days=self.LOAN_PERIOD_DAYS), returned_on=None))

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
        if isbn not in member.borrowed_books:
            raise ValueError("Book not borrowed by this member")
        loan = next(loan for loan in self.loans
                    if loan["member_id"] == member_id and loan["isbn"] == isbn
                    and loan.get("returned_on") is None)
        returned_on = self._resolve_date(returned_on, "Return")
        if returned_on < loan["borrowed_on"]:
            raise ValueError("Return cannot be before borrowing")
        member.return_book(isbn)
        book.return_copy()
        loan["returned_on"] = returned_on

    def search_by_title(self, title):
        return self._search_text("title", title)

    def search_by_author(self, author):
        return self._search_text("author", author)

    def get_available_books(self):
        return [book for book in self.catalog.values() if book.is_available()]

    def calculate_late_fees(self, member_id, as_of=None):
        self._get_member(member_id)
        as_of = self._resolve_date(as_of, "Report")
        return sum(self._loan_fee(loan, as_of)
                   for loan in self.loans if loan["member_id"] == member_id)

    @staticmethod
    def _loan_fee(loan, as_of):
        end = min(as_of, loan.get("returned_on") or as_of)
        return max(0, (end - loan["due_on"]).days) * Library.DAILY_LATE_FEE

    def member_history(self, member_id):
        self._get_member(member_id)
        return [dict(loan) for loan in self.loans if loan["member_id"] == member_id]

    def most_borrowed_book(self):
        counts = Counter(loan["isbn"] for loan in self.loans)
        if not counts:
            return None
        return self.catalog[max(sorted(counts), key=counts.get)]

    def search_books(self, *, genre=None, publication_year=None, rating=None, sort_by="title"):
        if sort_by not in ("title", "author", "publication_year", "rating"):
            raise ValueError("Unsupported sort field")
        matches = [book for book in self.catalog.values()
                if (genre is None or book.genre == genre)
                and (publication_year is None or book.publication_year == publication_year)
                and (rating is None or book.rating == rating)]
        def sort_key(book):
            value = getattr(book, sort_by)
            if isinstance(value, str):
                value = value.casefold()
            return value is None, value, book.isbn
        return sorted(matches, key=sort_key)

    def _search_text(self, field, text):
        return [book for book in self.catalog.values()
                if text.casefold() in getattr(book, field).casefold()]

    @staticmethod
    def _resolve_date(value, name):
        if value is None:
            return date.today()
        if type(value) is not date:
            raise ValueError(f"{name} date must be a date")
        return value
