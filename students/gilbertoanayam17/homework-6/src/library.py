"""Library: the catalog, its members, and the loans between them."""

from . import errors


class Library:
    """Coordinates books and members so every loan follows the library's rules."""

    def __init__(self):
        self._books = {}
        self._members = {}

    def add_book(self, book):
        """Add a book to the catalog, indexed by its ISBN."""
        self._books[book.isbn] = book

    def get_book(self, isbn):
        """Return the catalog entry for this ISBN."""
        if isbn not in self._books:
            raise errors.BookNotFoundError(f"No book with ISBN {isbn}")

        return self._books[isbn]

    def register_member(self, member):
        """Register a member, indexed by their id."""
        self._members[member.member_id] = member

    def get_member(self, member_id):
        """Return the registered member with this id."""
        if member_id not in self._members:
            raise errors.MemberNotFoundError(f"No member with id {member_id}")

        return self._members[member_id]

    def borrow_book(self, member_id, isbn):
        """Lend one copy of a book to a member."""
        member = self.get_member(member_id)
        if not member.can_borrow():
            raise errors.BorrowLimitExceededError(f"{member.name} already holds {member.max_borrow_limit} books")
        self.get_book(isbn).borrow()
        member.add_borrowed_book(isbn)
