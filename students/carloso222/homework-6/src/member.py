"""Member entity: a registered person who borrows books."""


class Member:
    """A library member with a borrow limit."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []

    def can_borrow(self):
        """Return True while the member is under their borrow limit."""
        return len(self.borrowed_books) < self.max_borrow_limit
