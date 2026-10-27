"""Library facade: catalog, members and lending rules."""

from src.exceptions import BookNotFoundError, MemberNotFoundError


class Library:
    """Coordinates books and members."""

    def __init__(self):
        self._books = {}
        self._members = {}

    def add_book(self, book):
        """Add ``book`` to the catalog."""
        if book.isbn in self._books:
            raise ValueError(f"A book with ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for ``isbn``."""
        if isbn not in self._books:
            raise BookNotFoundError(f"No book with ISBN {isbn}")
        return self._books[isbn]

    def register_member(self, member):
        """Register ``member`` so they can borrow books."""
        if member.member_id in self._members:
            raise ValueError(f"Member {member.member_id} is already registered")
        self._members[member.member_id] = member

    def get_member(self, member_id):
        """Return the registered member with ``member_id``."""
        if member_id not in self._members:
            raise MemberNotFoundError(f"No member with id {member_id}")
        return self._members[member_id]
