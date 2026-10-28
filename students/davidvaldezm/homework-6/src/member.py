"""Member domain model."""


class Member:
    """Member behavior developed test first."""

    def __init__(self, member_id, name, max_borrow_limit=3):
        if not isinstance(member_id, str) or not member_id.strip():
            raise ValueError('Member ID is required')
        if not isinstance(name, str) or not name.strip():
            raise ValueError('Member name is required')
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []
