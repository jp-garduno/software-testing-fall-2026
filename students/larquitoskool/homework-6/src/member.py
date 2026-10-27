class Member:
    LIMITS = {"Student": 3, "Public": 2, "Faculty": 5}
    
    def __init__(self, member_id, name, category="Public"):
        if category not in self.LIMITS:
            raise ValueError("Invalid category")
        self.member_id = member_id
        self.name = name
        self.category = category
        self.borrowed_books = []
        self.max_borrow_limit = self.LIMITS[category]
        self.late_fees = 0.0

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            
    def calculate_late_fee(self, days_borrowed):
        if days_borrowed > 14:
            self.late_fees += (days_borrowed - 14) * 1.0