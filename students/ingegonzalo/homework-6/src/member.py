class Member:
    CATEGORY_RULES = {
        "student": {"limit": 3, "late_fee_rate": 1},
        "faculty": {"limit": 5, "late_fee_rate": 0.5},
        "public": {"limit": 2, "late_fee_rate": 2},
    }

    def __init__(self, member_id, name, max_borrow_limit=None, category="student"):
        self._validate_name(name)
        self._validate_category(category)
        rules = self.CATEGORY_RULES[category]
        self.member_id = member_id
        self.name = name
        self.category = category
        self.borrowed_books = []
        self.max_borrow_limit = (
            rules["limit"] if max_borrow_limit is None else max_borrow_limit
        )
        self.late_fee_rate = rules["late_fee_rate"]
        self.late_fees = 0

    @staticmethod
    def _validate_name(name):
        if not name or not name.strip():
            raise ValueError("Name is required")

    @classmethod
    def _validate_category(cls, category):
        if category not in cls.CATEGORY_RULES:
            raise ValueError(f"Invalid category: {category}")

    def _has_borrowed(self, isbn):
        return isbn in self.borrowed_books

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        if self._has_borrowed(isbn):
            raise ValueError("Book already borrowed by this member")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        if not self._has_borrowed(isbn):
            raise ValueError("Book was not borrowed by this member")
        self.borrowed_books.remove(isbn)

    def add_late_fee(self, amount):
        self.late_fees += amount