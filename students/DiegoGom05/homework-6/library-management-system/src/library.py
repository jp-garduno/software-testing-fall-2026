class Library:
    def __init__(self):
        self._books = {}
        self._members = {}

    def get_available_books(self):
        return [b for b in self._books.values() if b.is_available()]

    def register_member(self, member):
        if member.member_id in self._members:
            raise ValueError("Member already registered")
        self._members[member.member_id] = member

    def get_member(self, member_id):
        return self._members[member_id]

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError("Book already in catalog")
        self._books[book.isbn] = book

    def borrow_book(self, member_id, isbn):
        if member_id not in self._members:
            raise ValueError("Member not found")

        if isbn not in self._books:
            raise ValueError("Book not found")

        member = self._members[member_id]
        book = self._books[isbn]

        if isbn in member.borrowed_books:
            raise ValueError("Member already borrowed this book")

        if not member.can_borrow():
            raise ValueError("Member reached borrow limit")

        book.borrow()
        member.add_borrowed_book(isbn)
