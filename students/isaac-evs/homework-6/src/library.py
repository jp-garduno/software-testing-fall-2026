from datetime import date, timedelta


class Library:
    def __init__(self, clock=date.today):
        self._clock = clock
        self._loans = {}
        self._books = {}
        self._members = {}

    def add_book(self, book):
        self._books[book.isbn] = book

    def register_member(self, member):
        self._members[member.member_id] = member

    def get_member(self, member_id):
        return self._require_member(member_id)

    def get_available_books(self):
        return [book for book in self._books.values() if book.is_available()]

    def borrow_book(self, member_id, isbn):
        member = self._require_member(member_id)
        book = self._require_book(isbn)
        if not book.is_available():
            raise ValueError("No copies available")
        member.add_borrowed_book(isbn)
        book.borrow()
        self._loans[(member_id, isbn)] = self._clock()

    def get_due_date(self, member_id, isbn):
        return self._loans[(member_id, isbn)] + timedelta(days=14)

    def return_book(self, member_id, isbn):
        member = self._require_member(member_id)
        book = self._require_book(isbn)
        member.return_book(isbn)
        book.return_copy()

    def calculate_late_fee(self, member_id, isbn):
        return 0

    def search_by_title(self, title):
        return self._search("title", title)

    def search_by_author(self, author):
        return self._search("author", author)

    def _search(self, field, term):
        term = term.lower()
        return [book for book in self._books.values() if term in getattr(book, field).lower()]

    def _require_member(self, member_id):
        if member_id not in self._members:
            raise ValueError("Member not found")
        return self._members[member_id]

    def _require_book(self, isbn):
        if isbn not in self._books:
            raise ValueError("Book not found")
        return self._books[isbn]
