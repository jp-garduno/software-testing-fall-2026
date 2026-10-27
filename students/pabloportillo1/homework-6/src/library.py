from datetime import date

from loan import Loan


class Library:
    def __init__(self, clock=date.today, notifier=None):
        self._clock = clock
        self._notifier = notifier
        self._books = {}
        self._members = {}
        self._loans = []
        self._queues = {}
        self._holds = {}

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError(f"ISBN {book.isbn} is already in the catalog")
        self._books[book.isbn] = book

    def get_book(self, isbn):
        if isbn not in self._books:
            raise LookupError(f"No book with ISBN {isbn}")
        return self._books[isbn]

    def register_member(self, member):
        if member.member_id in self._members:
            raise ValueError(f"Member {member.member_id} is already registered")
        self._members[member.member_id] = member

    def get_member(self, member_id):
        if member_id not in self._members:
            raise LookupError(f"No member with id {member_id}")
        return self._members[member_id]

    def borrow_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        book.ensure_available()
        held = self._holds.get(isbn, [])
        if member_id not in held and self._free_copies(book) == 0:
            raise ValueError(f"The copy of '{book.title}' is held for another member")
        member.add_borrowed_book(isbn)
        book.borrow()
        if member_id in held:
            held.remove(member_id)
        loan = Loan(member_id, isbn, self._clock())
        self._loans.append(loan)
        return loan

    def return_book(self, member_id, isbn):
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        member.return_book(isbn)
        book.return_copy()
        self._active_loan(member_id, isbn).returned_on = self._clock()
        self._hold_for_next_reserver(book)

    def search_by_title(self, title):
        return self._search_text("title", title)

    def search_by_author(self, author):
        return self._search_text("author", author)

    def _search_text(self, field, text):
        wanted = text.casefold()
        return [book for book in self._books.values() if wanted in getattr(book, field).casefold()]

    def get_available_books(self):
        return [book for book in self._books.values() if book.is_available()]

    def calculate_late_fees(self, member_id):
        rate = self.get_member(member_id).category.daily_late_fee_cents
        today = self._clock()
        return sum(loan.days_overdue(today) * rate for loan in self._loans if loan.member_id == member_id)

    def _active_loan(self, member_id, isbn):
        return next(
            loan
            for loan in self._loans
            if loan.member_id == member_id and loan.isbn == isbn and loan.returned_on is None
        )

    def reserve_book(self, member_id, isbn):
        self.get_member(member_id)
        book = self.get_book(isbn)
        if self._free_copies(book) > 0:
            raise ValueError(f"'{book.title}' is available, borrow it instead")
        queue = self._queues.setdefault(isbn, [])
        if member_id in queue:
            raise ValueError(f"{member_id} has already reserved '{book.title}'")
        queue.append(member_id)

    def reservations_for(self, isbn):
        return list(self._queues.get(isbn, []))

    def _free_copies(self, book):
        return book.available_copies - len(self._holds.get(book.isbn, []))

    def _hold_for_next_reserver(self, book):
        queue = self._queues.get(book.isbn)
        if not queue:
            return
        next_member_id = queue.pop(0)
        self._holds.setdefault(book.isbn, []).append(next_member_id)
        if self._notifier is not None:
            self._notifier.notify_available(self.get_member(next_member_id), book)

    def search(self, genre=None, year=None, min_rating=None):
        return [book for book in self._books.values() if _matches(book.details, genre, year, min_rating)]


def _matches(details, genre, year, min_rating):
    if genre is not None and details.genre != genre:
        return False
    if year is not None and details.year != year:
        return False
    return min_rating is None or (details.rating is not None and details.rating >= min_rating)
