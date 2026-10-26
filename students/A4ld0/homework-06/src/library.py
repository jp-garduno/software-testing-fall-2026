"""Catalog and lending operations."""


class Library:
    def __init__(self):
        self.catalog = {}
        self.members = {}

    def add_book(self, book):
        if book.isbn in self.catalog:
            raise ValueError("ISBN already registered")
        self.catalog[book.isbn] = book

    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError("Duplicate member ID")
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        member = self._get_member(member_id)
        book = self._get_book(isbn)
        if not member.can_borrow():
            raise ValueError("Member borrowing limit reached")
        book.borrow()
        member.add_borrowed_book(isbn)

    def _get_member(self, member_id):
        if member_id not in self.members:
            raise ValueError("Unknown member")
        return self.members[member_id]

    def _get_book(self, isbn):
        if isbn not in self.catalog:
            raise ValueError("Unknown ISBN")
        return self.catalog[isbn]

    def return_book(self, member_id, isbn):
        member = self._get_member(member_id)
        book = self._get_book(isbn)
        member.return_book(isbn)
        book.return_copy()
