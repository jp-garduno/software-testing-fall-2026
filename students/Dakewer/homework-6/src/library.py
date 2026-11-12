from collections import Counter
from datetime import date, timedelta

from src.history import HistoryEvent

LOAN_DAYS = 14


class Library:
    def __init__(self):
        self._books = {}
        self._members = {}
        self._loans = {}
        self._history = []

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError("Book already in catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        if isbn not in self._books:
            raise ValueError("Unknown book")
        return self._books[isbn]

    def register_member(self, member):
        if member.member_id in self._members:
            raise ValueError("Member already registered")
        self._members[member.member_id] = member

    def get_member(self, member_id):
        if member_id not in self._members:
            raise ValueError("Unknown member")
        return self._members[member_id]

    def borrow_book(self, member_id, isbn, borrow_date=None):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        if not book.is_available():
            raise ValueError("No copies available")
        member.add_borrowed_book(isbn)
        book.borrow()
        borrow_date = borrow_date or date.today()
        self._loans[(member_id, isbn)] = borrow_date
        self._history.append(HistoryEvent(member_id, isbn, "borrow", borrow_date))

    def return_book(self, member_id, isbn, return_date=None):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        return_date = return_date or date.today()
        fee = self._loan_fee(member_id, isbn, return_date)
        member.return_book(isbn)
        book.return_copy()
        del self._loans[(member_id, isbn)]
        self._history.append(HistoryEvent(member_id, isbn, "return", return_date))
        return fee

    def search_by_title(self, title):
        return self._search("title", title)

    def search_by_author(self, author):
        return self._search("author", author)

    def get_available_books(self):
        return [book for book in self._books.values() if book.is_available()]

    def _search(self, field, query):
        if not query.strip():
            raise ValueError("Search query cannot be empty")
        needle = query.lower()
        return [b for b in self._books.values() if needle in getattr(b, field).lower()]

    def get_due_date(self, member_id, isbn):
        return self._loans[(member_id, isbn)] + timedelta(days=LOAN_DAYS)

    def calculate_late_fee(self, member_id, as_of):
        return sum(
            self._loan_fee(loan_member, isbn, as_of)
            for loan_member, isbn in self._loans
            if loan_member == member_id
        )

    def _loan_fee(self, member_id, isbn, as_of):
        due = self.get_due_date(member_id, isbn)
        rate = self.get_member(member_id).late_fee_rate
        return max(0, (as_of - due).days) * rate

    def get_history(self, member_id):
        return [e for e in self._history if e.member_id == member_id]

    def member_history_report(self, member_id):
        member = self.get_member(member_id)
        events = self.get_history(member_id)
        return {
            "member_id": member_id,
            "name": member.name,
            "total_borrows": sum(1 for e in events if e.action == "borrow"),
            "total_returns": sum(1 for e in events if e.action == "return"),
            "currently_borrowed": list(member.borrowed_books),
        }

    def most_borrowed_book(self):
        counts = Counter(e.isbn for e in self._history if e.action == "borrow")
        if not counts:
            return None
        return counts.most_common(1)[0][0]
