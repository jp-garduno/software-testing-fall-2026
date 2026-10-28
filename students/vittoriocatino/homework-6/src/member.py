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
