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
