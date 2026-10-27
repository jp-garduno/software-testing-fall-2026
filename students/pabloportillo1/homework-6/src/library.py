class Library:
    def __init__(self):
        self._books = {}
        self._members = {}

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError(f"ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        return self._books[isbn]

    def register_member(self, member):
        self._members[member.member_id] = member

    def get_member(self, member_id):
        return self._members[member_id]
