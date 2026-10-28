class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError("Member with this ID already registered")
        self.members[member.member_id] = member

    def get_member(self, member_id):
        if member_id not in self.members:
            raise ValueError(f"Member {member_id} is not registered")
        return self.members[member_id]

    def add_book(self, book):
        if book.isbn in self.books:
            raise ValueError("Book with this ISBN already exists")
        self.books[book.isbn] = book

    def get_available_books(self):
        return [book for book in self.books.values() if book.is_available()]

    def borrow_book(self, member_id, isbn):
        self.books[isbn].borrow()