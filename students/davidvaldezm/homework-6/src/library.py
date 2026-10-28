"""Library domain model."""


class Library:
    """Library behavior developed test first."""

    def __init__(self):
        self.catalog = {}
        self.members = {}

    def add_book(self, book):
        if book.isbn in self.catalog:
            raise ValueError('ISBN already registered')
        self.catalog[book.isbn] = book

    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError('Member already registered')
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        if member_id not in self.members:
            raise ValueError('Unknown member')
        member = self.members[member_id]
        if isbn not in self.catalog:
            raise ValueError('Unknown book')
        book = self.catalog[isbn]
        if not member.can_borrow():
            raise ValueError('Borrow limit reached')
        if isbn in member.borrowed_books:
            raise ValueError('Book already borrowed by this member')
        book.borrow()
        member.add_borrowed_book(isbn)

    def return_book(self, member_id, isbn):
        if member_id not in self.members:
            raise ValueError('Unknown member')
        member = self.members[member_id]
        book = self.catalog[isbn]
        member.return_book(isbn)
        book.return_copy()
