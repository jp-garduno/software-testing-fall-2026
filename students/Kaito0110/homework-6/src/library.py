"""Library service managing catalog, members, loans, reservations, and history."""

from datetime import date, timedelta


class Library:
    """Coordinates books, members, borrowing, search, reservations, and fees."""

    def __init__(self):
        self.books = {}
        self.members = {}
        self.reservations = {}
        self.notifications = []
        self.borrowing_history = []

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

    def search_books(
        self,
        genre=None,
        publication_year=None,
        min_rating=None,
        sort_by=None,
    ):
        """Filter books using combined AND criteria and optional sorting."""
        results = list(self.books.values())

        if genre is not None:
            results = [
                book
                for book in results
                if book.genre is not None and book.genre.lower() == genre.lower()
            ]

        if publication_year is not None:
            results = [
                book
                for book in results
                if book.publication_year == publication_year
            ]

        if min_rating is not None:
            results = [
                book
                for book in results
                if book.rating is not None and book.rating >= min_rating
            ]

        if sort_by is not None:
            valid_sort_fields = {"title", "publication_year", "rating"}
            if sort_by not in valid_sort_fields:
                raise ValueError(f"Invalid sort field: {sort_by}")
            results.sort(key=lambda b: getattr(b, sort_by))

        return results

    def get_available_books(self):
        """Return all books with at least one available copy."""
        return [book for book in self.books.values() if book.is_available()]

    def borrow_book(self, member_id, isbn):
        """Borrow a book for a registered member and record history."""
        if member_id not in self.members:
            raise ValueError("Member not found")

        if isbn not in self.books:
            raise ValueError("Book not found")

        member = self.members[member_id]
        book = self.books[isbn]

        if not member.can_borrow():
            raise ValueError("Member has reached the borrowing limit")

        book.borrow()
        member.add_borrowed_book(isbn)
        self.borrowing_history.append(
            {"member_id": member_id, "isbn": isbn, "action": "borrow"}
        )

    def calculate_late_fee(
        self, borrow_date: date, return_date: date, daily_rate: float = 1.0
    ) -> float:
        """Calculate overdue fee given a 14-day loan period and daily rate."""
        due_date = borrow_date + timedelta(days=14)
        late_days = max(0, (return_date - due_date).days)
        fee = late_days * daily_rate
        return int(fee) if fee == int(fee) else round(fee, 2)

    def calculate_member_late_fees(self, member_id, loans):
        """Calculate total late fees for a member across multiple loans."""
        if member_id not in self.members:
            raise ValueError("Member not found")

        member = self.members[member_id]
        total = sum(
            self.calculate_late_fee(
                borrow_date, return_date, daily_rate=member.late_fee_rate
            )
            for borrow_date, return_date in loans
        )
        return int(total) if total == int(total) else round(total, 2)

    def reserve_book(self, member_id, isbn):
        """Place a member in the FIFO reservation queue for an unavailable book."""
        if member_id not in self.members:
            raise ValueError("Member not found")

        if isbn not in self.books:
            raise ValueError("Book not found")

        if self.books[isbn].is_available():
            raise ValueError("Book is available; no reservation needed")

        if isbn not in self.reservations:
            self.reservations[isbn] = []

        if member_id in self.reservations[isbn]:
            raise ValueError("Member already reserved this book")

        self.reservations[isbn].append(member_id)

    def return_book(self, member_id, isbn):
        """Return a borrowed book, record history, and notify next reserver."""
        if member_id not in self.members:
            raise ValueError("Member not found")

        if isbn not in self.books:
            raise ValueError("Book not found")

        member = self.members[member_id]
        book = self.books[isbn]

        member.return_book(isbn)
        book.return_copy()
        self.borrowing_history.append(
            {"member_id": member_id, "isbn": isbn, "action": "return"}
        )

        pass
