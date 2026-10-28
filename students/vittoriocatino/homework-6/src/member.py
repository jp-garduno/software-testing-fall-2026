"""Library member domain entity."""


class Member:
    """A member permitted to borrow up to a configured number of books."""

    CATEGORY_RULES = {
        "student": (3, 1.0),
        "faculty": (5, 0.5),
        "public": (2, 1.5),
    }

    def __init__(
        self,
        member_id: str,
        name: str,
        max_borrow_limit: int | None = None,
        category: str = "student",
    ) -> None:
        if category not in self.CATEGORY_RULES:
            raise ValueError("unknown member category")
        category_limit, self.late_fee_rate = self.CATEGORY_RULES[category]
        if max_borrow_limit is None:
            max_borrow_limit = category_limit
        if not member_id or not name.strip() or max_borrow_limit < 1:
            raise ValueError("member requires identity, name, and positive limit")
        self.member_id = member_id
        self.name = name
        self.category = category
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books: list[str] = []

    def can_borrow(self) -> bool:
        """Return whether the borrow limit permits one more book."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn: str) -> None:
        """Record an ISBN after enforcing the member's limit."""
        if not self.can_borrow():
            raise ValueError("borrow limit reached")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn: str) -> None:
        """Remove a borrowed ISBN, rejecting untracked returns."""
        if isbn not in self.borrowed_books:
            raise ValueError("book is not borrowed by this member")
        self.borrowed_books.remove(isbn)
