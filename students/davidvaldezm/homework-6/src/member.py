"""Member domain model."""


class Member:
    """Member behavior developed test first."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []
