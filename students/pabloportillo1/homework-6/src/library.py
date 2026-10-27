class Library:
    def __init__(self):
        self._books = {}

    def add_book(self, book):
        self._books[book.isbn] = book

    def get_book(self, isbn):
        return self._books[isbn]
