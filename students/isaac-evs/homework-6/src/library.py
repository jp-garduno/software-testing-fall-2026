class Library:
    def __init__(self):
        self._books = {}
        self._members = {}

    def add_book(self, book):
        self._books[book.isbn] = book

    def get_available_books(self):
        return [book for book in self._books.values() if book.is_available()]

    def register_member(self, member):
        self._members[member.member_id] = member

    def get_member(self, member_id):
        return self._members[member_id]

    def borrow_book(self, member_id, isbn):
        member = self._require_member(member_id)
        book = self._require_book(isbn)
        member.add_borrowed_book(isbn)
        book.borrow()

    def _require_member(self, member_id):
        if member_id not in self._members:
            raise ValueError("Member not found")
        return self._members[member_id]

    def _require_book(self, isbn):
        if isbn not in self._books:
            raise ValueError("Book not found")
        return self._books[isbn]
