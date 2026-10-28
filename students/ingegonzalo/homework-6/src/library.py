class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    # --- catálogo ---
    def add_book(self, book):
        if book.isbn in self.books:
            raise ValueError("Book with this ISBN already exists")
        self.books[book.isbn] = book

    def _get_book(self, isbn):
        if isbn not in self.books:
            raise ValueError(f"Book {isbn} is not in the catalog")
        return self.books[isbn]

    def get_available_books(self):
        return [book for book in self.books.values() if book.is_available()]

    # --- miembros ---
    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError("Member with this ID already registered")
        self.members[member.member_id] = member

    def get_member(self, member_id):
        if member_id not in self.members:
            raise ValueError(f"Member {member_id} is not registered")
        return self.members[member_id]

    # --- préstamos ---
    def borrow_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self._get_book(isbn)
        if not book.is_available():
            raise ValueError("No copies available")
        member.add_borrowed_book(isbn)
        book.borrow()

    def return_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self._get_book(isbn)
        member.return_book(isbn)
        book.return_copy()

    # --- búsquedas ---
    def search_by_title(self, title):
        return self._search_by("title", title)

    def search_by_author(self, author):
        return self._search_by("author", author)

    def _search_by(self, attribute, text):
        query = text.lower()
        return [
            book for book in self.books.values()
            if query in getattr(book, attribute).lower()
        ]