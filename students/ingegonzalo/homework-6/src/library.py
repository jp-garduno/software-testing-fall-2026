class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        self.books[book.isbn] = book

    def get_available_books(self):
        return [book for book in self.books.values() if book.is_available()]