"""Member domain model."""

from decimal import Decimal


class Member:
    """Member behavior developed test first."""

    CATEGORY_LIMITS = {"student": 3, "faculty": 5, "public": 2}

    def __init__(self, member_id, name, max_borrow_limit=None, category="student"):
        if not isinstance(category, str) or category not in self.CATEGORY_LIMITS:
            raise ValueError("Unknown member category")
        self.category = category
        if max_borrow_limit is None:
            max_borrow_limit = self.CATEGORY_LIMITS[category]
        if not isinstance(member_id, str) or not member_id.strip():
            raise ValueError("Member ID is required")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name is required")
        if (
            not isinstance(max_borrow_limit, int)
            or isinstance(max_borrow_limit, bool)
            or max_borrow_limit < 1
        ):
            raise ValueError("Borrow limit must be a positive integer")
        self.member_id = member_id
        self.name = name
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []

    def can_borrow(self):
        """Return whether another distinct book fits the borrowing limit."""
        return len(self.borrowed_books) < self.max_borrow_limit

    def validate_borrow(self, isbn):
        """Check borrowing constraints before changing any state."""
        if isbn in self.borrowed_books:
            raise ValueError("Book already borrowed by this member")
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")

    def add_borrowed_book(self, isbn):
        """Record a distinct ISBN if borrowing is allowed."""
        self.validate_borrow(isbn)
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        """Remove a borrowed ISBN or raise ValueError."""
        if isbn not in self.borrowed_books:
            raise ValueError("Book not borrowed by this member")
        self.borrowed_books.remove(isbn)

    @property
    def daily_fee_rate(self):
        """Return the category policy as an exact decimal dollar amount."""
        rates = {"student": "1", "faculty": "0.50", "public": "1.50"}
        return Decimal(rates[self.category])
