from datetime import date

from loan import Loan


class Library:
    def __init__(self, clock=date.today):
        self._clock = clock
        self._books = {}
        self._members = {}

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError(f"ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        if isbn not in self._books:
            raise LookupError(f"No book with ISBN {isbn}")
        return self._books[isbn]

    def register_member(self, member):
        if member.member_id in self._members:
            raise ValueError(f"Member {member.member_id} is already registered")
        self._members[member.member_id] = member

    def get_member(self, member_id):
        if member_id not in self._members:
            raise LookupError(f"No member with id {member_id}")
        return self._members[member_id]

    def borrow_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        book.ensure_available()
        member.add_borrowed_book(isbn)
        book.borrow()
        return Loan(member_id, isbn, self._clock())

    def return_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        member.return_book(isbn)
        book.return_copy()

    def search_by_title(self, title):
        return self._search_text("title", title)

    def search_by_author(self, author):
        return self._search_text("author", author)

    def _search_text(self, field, text):
        wanted = text.casefold()
        return [book for book in self._books.values() if wanted in getattr(book, field).casefold()]

    def get_available_books(self):
        return [book for book in self._books.values() if book.is_available()]
