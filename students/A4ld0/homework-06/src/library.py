"""Catalog and lending operations."""


class Library:
    def __init__(self):
        self.catalog = {}
        self.members = {}

    def add_book(self, book):
        self.catalog[book.isbn] = book
