from enum import Enum
from typing import NamedTuple


class CategoryPolicy(NamedTuple):
    borrow_limit: int
    late_fee_per_day: float


class MemberCategory(Enum):
    STUDENT = CategoryPolicy(3, 1.00)
    FACULTY = CategoryPolicy(5, 0.50)
    PUBLIC = CategoryPolicy(2, 1.50)

    @property
    def borrow_limit(self):
        return self.value.borrow_limit

    @property
    def late_fee_per_day(self):
        return self.value.late_fee_per_day


class Member:
    def __init__(self, member_id, name, max_borrow_limit=None, category=MemberCategory.STUDENT):
        self.member_id = member_id
        self.name = name
        self.category = category
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit if max_borrow_limit is not None else category.borrow_limit

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow_limit

    def add_borrowed_book(self, isbn):
        if self._holds(isbn):
            raise ValueError("Book already borrowed")
        if not self.can_borrow():
            raise ValueError("Borrow limit reached")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        if not self._holds(isbn):
            raise ValueError("Book not borrowed by this member")
        self.borrowed_books.remove(isbn)

    def _holds(self, isbn):
        return isbn in self.borrowed_books
