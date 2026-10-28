CATEGORY_LIMITS = {"student": 3, "faculty": 5, "public": 2}
CATEGORY_FEE_RATES = {"student": 1.0, "faculty": 0.5, "public": 2.0}


class Member:
    def __init__(self, member_id, name, max_borrow_limit=None, category="student"):
        if category not in CATEGORY_LIMITS:
            raise ValueError(f"Unknown category: {category}")
        self._validate_identity(member_id, name)
        self.member_id = member_id
        self.name = name
        if max_borrow_limit is None:
            max_borrow_limit = CATEGORY_LIMITS[category]
        self.max_borrow_limit = max_borrow_limit
        self.late_fee_rate = CATEGORY_FEE_RATES[category]
        self.borrowed_books = []

    @staticmethod
    def _validate_identity(member_id, name):
        if not member_id:
            raise ValueError("Member id is required")
        if not name or not name.strip():
            raise ValueError("Member name is required")

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        if isbn in self.borrowed_books:
            raise ValueError("Book already borrowed by this member")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        if isbn not in self.borrowed_books:
            raise ValueError("Book was not borrowed by this member")
        self.borrowed_books.remove(isbn)
