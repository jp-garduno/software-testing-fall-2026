"""Member model for Library Management System."""


class Member:
    """Represents a registered library member."""

    def __init__(
        self,
        member_id: str,
        name: str,
        max_borrow_limit: int = 3,
    ) -> None:
        if not member_id or not str(member_id).strip():
            raise ValueError("Member ID is required")
        if not name or not str(name).strip():
            raise ValueError("Member name is required")
        if int(max_borrow_limit) <= 0:
            raise ValueError("Max borrow limit must be positive")

        self.member_id = str(member_id).strip()
        self.name = str(name).strip()
        self.max_borrow_limit = int(max_borrow_limit)
        self.borrowed_books: list[str] = []
