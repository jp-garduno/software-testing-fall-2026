class Library:
    def __init__(self):
        self.catalog = {}
        self.members = {}

    def add_book(self, book):
        self.catalog[book.isbn] = book

    def register_member(self, member):
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        member = self.members.get(member_id)
        book = self.catalog.get(isbn)
        if not member or not book:
            raise ValueError("Member or Book not found")
        
        member.add_borrowed_book(isbn)
        book.borrow()

    def return_book(self, member_id, isbn, days_borrowed=0):
        member = self.members.get(member_id)
        book = self.catalog.get(isbn)
        if member and book:
            member.return_book(isbn)
            book.return_copy()
            member.calculate_late_fee(days_borrowed)

    def search_books(self, title=None, author=None):
        results = list(self.catalog.values())
        if title:
            results = [b for b in results if title.lower() in b.title.lower()]
        if author:
            results = [b for b in results if author.lower() in b.author.lower()]
        return results

    def get_available_books(self):
        return [b for b in self.catalog.values() if b.is_available()]