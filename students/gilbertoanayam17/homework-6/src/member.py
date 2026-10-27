"""Member: who can borrow, how many books at once, and which books they hold."""


class Member:
    """A registered library user."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit

    def add_borrowed_book(self, isbn):
        """Record that the member took a copy of this book."""
        self.borrowed_books.append(isbn)
