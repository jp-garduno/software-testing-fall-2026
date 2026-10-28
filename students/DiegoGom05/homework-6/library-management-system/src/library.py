from datetime import date, timedelta
from collections import Counter


class Library:
    LOAN_PERIOD_DAYS = 14

    def __init__(self):
        self._books = {}
        self._members = {}
        self._loans = {}
        self._history = []

    def get_available_books(self):
        return [b for b in self._books.values() if b.is_available()]

    def register_member(self, member):
        if member.member_id in self._members:
            raise ValueError("Member already registered")

        self._members[member.member_id] = member

    def _find_member(self, member_id):
        if member_id not in self._members:
            raise ValueError("Member not found")

        return self._members[member_id]

    def _find_book(self, isbn):
        if isbn not in self._books:
            raise ValueError("Book not found")

        return self._books[isbn]

    def get_member(self, member_id):
        return self._members[member_id]

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError("Book already in catalog")

        self._books[book.isbn] = book

    def borrow_book(self, member_id, isbn, borrow_date=None):
        borrow_date = borrow_date or date.today()

        member = self._find_member(member_id)
        book = self._find_book(isbn)

        if isbn in member.borrowed_books:
            raise ValueError("Member already borrowed this book")

        if not member.can_borrow():
            raise ValueError("Member reached borrow limit")

        book.borrow()
        member.add_borrowed_book(isbn)
        self._loans[(member_id, isbn)] = borrow_date
        self._history.append(
            {
                "member_id": member_id,
                "isbn": isbn,
                "action": "borrow",
                "date": borrow_date,
            }
        )

    def return_book(self, member_id, isbn, return_date=None):
        member = self._find_member(member_id)
        book = self._find_book(isbn)
        return_date = return_date or date.today()

        member.return_book(isbn)
        book.return_copy()

        self._loans.pop((member_id, isbn), None)
        self._history.append(
            {
                "member_id": member_id,
                "isbn": isbn,
                "action": "return",
                "date": return_date,
            }
        )

    def search_by_title(self, title):
        return self._search("title", title)

    def search_by_author(self, author):
        return self._search("author", author)

    def _search(self, field, text):
        text = text.lower()

        return [
            book
            for book in self._books.values()
            if text in getattr(book, field).lower()
        ]

    @classmethod
    def _due_date(cls, borrowed_on):
        return borrowed_on + timedelta(days=cls.LOAN_PERIOD_DAYS)

    def calculate_late_fees(self, member_id, today=None):
        today = today or date.today()
        member = self._find_member(member_id)
        total = 0

        for (owner, _isbn), borrowed_on in self._loans.items():
            if owner != member_id:
                continue

            due = self._due_date(borrowed_on)
            days_late = (today - due).days

            if days_late > 0:
                total += days_late * member.late_fee_rate

        return total

    def get_member_history(self, member_id):
        return [e for e in self._history if e["member_id"] == member_id]

    def most_borrowed_book(self):
        counts = Counter(e["isbn"] for e in self._history if e["action"] == "borrow")
        if not counts:
            return None
        return counts.most_common(1)[0][0]

    def generate_member_report(self, member_id):
        member = self._find_member(member_id)
        lines = [f"History for {member.name}"]
        lines += [f"{e['date']} {e['action']} {e['isbn']}"
                  for e in self.get_member_history(member_id)]
        return "\n".join(lines)
