"""Library member domain entity."""


class Member:
    """A member permitted to borrow up to a configured number of books."""

    def __init__(self, member_id: str, name: str, max_borrow_limit: int = 3) -> None:
        if not member_id or not name.strip() or max_borrow_limit < 1:
            raise ValueError("member requires identity, name, and positive limit")
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books: list[str] = []
