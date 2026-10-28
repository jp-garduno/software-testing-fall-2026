class Library:
    def __init__(self):
        self._books = {}
        self._members = {}

    def register_member(self, member):
        self._members[member.member_id] = member

    def get_member(self, member_id):
        return self._members[member_id]

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError("Book already in catalog")
        self._books[book.isbn] = book

    def get_available_books(self):
        return [b for b in self._books.values() if b.is_available()]
