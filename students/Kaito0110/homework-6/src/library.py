"""Library service managing catalog, members, loans, reservations, and history."""


class Library:
    """Coordinates books, members, borrowing, search, reservations, and fees."""

    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, book):
        """Add a new book to the catalog."""
        if book.isbn in self.books:
            raise ValueError("Book ISBN already exists")

        self.books[book.isbn] = book

    def register_member(self, member):
        """Register a new library member."""
        if member.member_id in self.members:
            raise ValueError("Member ID already exists")

        self.members[member.member_id] = member

    def search_by_title(self, title):
        """Search books by case-insensitive partial title match."""
        return [
            book
            for book in self.books.values()
            if title.lower() in book.title.lower()
        ]

    def search_by_author(self, author):
        """Search books by case-insensitive partial author match."""
        return [
            book
            for book in self.books.values()
            if author.lower() in book.author.lower()
        ]

    def get_available_books(self):
        """Return all books with at least one available copy."""
        return [book for book in self.books.values() if book.is_available()]
