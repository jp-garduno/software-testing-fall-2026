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
        if member_id not in self.members:
            raise ValueError("Unknown member")
        member = self.members[member_id]
        book = self.catalog[isbn]
        book.borrow()
        member.add_borrowed_book(isbn)
