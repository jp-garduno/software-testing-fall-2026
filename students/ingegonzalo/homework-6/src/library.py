class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def register_member(self, member):
        self.members[member.member_id] = member

    def get_member(self, member_id):
        return self.members[member_id]

    def add_book(self, book):
        if book.isbn in self.books:
            raise ValueError("Book with this ISBN already exists")
        self.books[book.isbn] = book

    def get_available_books(self):
        return [book for book in self.books.values() if book.is_available()]