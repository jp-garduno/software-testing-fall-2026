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
        self.members[member.member_id] = member
