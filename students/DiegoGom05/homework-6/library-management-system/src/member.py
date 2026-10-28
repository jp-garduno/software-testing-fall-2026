CATEGORY_RULES = {
    "student": {"limit": 3, "late_fee_rate": 1.0},
    "faculty": {"limit": 5, "late_fee_rate": 0.5},
    "public":  {"limit": 2, "late_fee_rate": 1.5},
}

class Member:

    def __init__(self, member_id, name, max_borrow_limit=None, category="student"):
        if category not in CATEGORY_RULES:
            raise ValueError(f"Invalid category: {category}")

        if max_borrow_limit is None:
            max_borrow_limit = CATEGORY_RULES[category]["limit"]

        self.late_fee_rate = CATEGORY_RULES[category]["late_fee_rate"]
        self.member_id = member_id
        self.name = name
        self.category = category
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []


    def add_borrowed_book(self, isbn):
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        self.borrowed_books.append(isbn)

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def return_book(self, isbn):
        if isbn not in self.borrowed_books:
            raise ValueError("Book not borrowed by member")
        self.borrowed_books.remove(isbn)
