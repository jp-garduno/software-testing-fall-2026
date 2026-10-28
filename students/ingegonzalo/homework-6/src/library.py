from collections import Counter
from datetime import date

from src.history import BORROW, RETURN, HistoryEntry
from src.late_fees import calculate_late_fee


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self._loans = {}
        self._history = []

    # --- catálogo ---
    def add_book(self, book):
        if book.isbn in self.books:
            raise ValueError("Book with this ISBN already exists")
        self.books[book.isbn] = book

    def _get_book(self, isbn):
        if isbn not in self.books:
            raise ValueError(f"Book {isbn} is not in the catalog")
        return self.books[isbn]

    def get_available_books(self):
        return [book for book in self.books.values() if book.is_available()]

    # --- miembros ---
    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError("Member with this ID already registered")
        self.members[member.member_id] = member

    def get_member(self, member_id):
        if member_id not in self.members:
            raise ValueError(f"Member {member_id} is not registered")
        return self.members[member_id]

    # --- préstamos ---
    def borrow_book(self, member_id, isbn, borrow_date=None):
        member = self.get_member(member_id)
        book = self._get_book(isbn)
        if not book.is_available():
            raise ValueError("No copies available")
        borrow_date = borrow_date or date.today()
        member.add_borrowed_book(isbn)
        book.borrow()
        self._loans[(member_id, isbn)] = borrow_date
        self._record(member_id, isbn, BORROW, borrow_date)

    def return_book(self, member_id, isbn, return_date=None):
        member = self.get_member(member_id)
        book = self._get_book(isbn)
        return_date = return_date or date.today()
        member.return_book(isbn)
        book.return_copy()
        borrow_date = self._loans.pop((member_id, isbn))
        fee = calculate_late_fee(borrow_date, return_date, member.late_fee_rate)
        member.add_late_fee(fee)
        self._record(member_id, isbn, RETURN, return_date)
        return fee

    # --- historial ---
    def _record(self, member_id, isbn, action, occurred_on):
        self._history.append(HistoryEntry(member_id, isbn, action, occurred_on))

    def get_history(self):
        return list(self._history)

    def get_member_history(self, member_id):
        self.get_member(member_id)
        return [e for e in self._history if e.member_id == member_id]

    def generate_member_report(self, member_id):
        member = self.get_member(member_id)
        lines = [f"History for {member.name} ({member.member_id})"]
        for entry in self.get_member_history(member_id):
            book = self._get_book(entry.isbn)
            lines.append(
                f"{entry.occurred_on.isoformat()} {entry.action.upper()} "
                f"{book.title} ({entry.isbn})"
            )
        return "\n".join(lines)

    def most_borrowed_book(self):
        counts = Counter(e.isbn for e in self._history if e.action == BORROW)
        if not counts:
            return None
        isbn, _ = counts.most_common(1)[0]
        return self.books[isbn]

    # --- búsquedas ---
    def search_by_title(self, title):
        return self._search_by("title", title)

    def search_by_author(self, author):
        return self._search_by("author", author)

    def _search_by(self, attribute, text):
        query = text.lower()
        return [
            book for book in self.books.values()
            if query in getattr(book, attribute).lower()
        ]