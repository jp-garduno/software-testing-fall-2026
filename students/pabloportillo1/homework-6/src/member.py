class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.max_borrow_limit = 3

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        if not self.can_borrow():
            raise ValueError(f"{self.name} has reached the borrow limit of {self.max_borrow_limit}")
        if isbn in self.borrowed_books:
            raise ValueError(f"{self.name} has already borrowed {isbn}")
        self.borrowed_books.append(isbn)
