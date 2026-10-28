BORROW_LIMITS = {"student": 3, "faculty": 5, "public": 2}

class Member:

    def __init__(self, member_id, name, max_borrow_limit=None, category="student"):
        if category not in BORROW_LIMITS:
            raise ValueError(f"Invalid category: {category}")

        if max_borrow_limit is None:
             max_borrow_limit = BORROW_LIMITS[category]
        self.member_id = member_id
        self.name = name
        self.category = category
        if max_borrow_limit is None:
            max_borrow_limit = 5 if category == "faculty" else 3
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
