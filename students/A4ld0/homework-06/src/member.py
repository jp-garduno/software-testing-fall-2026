"""Members and borrowing limits."""


class Member:
    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        self.borrowed_books.append(isbn)
