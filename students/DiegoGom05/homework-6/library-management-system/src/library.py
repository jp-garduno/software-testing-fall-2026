class Library:
    def __init__(self):
        self._books = {}

    def add_book(self, book):
        self._books[book.isbn] = book

    def get_available_books(self):
        return [b for b in self._books.values() if b.is_available()]
