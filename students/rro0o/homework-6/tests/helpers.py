"""Shared helpers for the tests."""

from datetime import date, timedelta

from src.book import Book
from src.library import Library
from src.member import Member
from src.member_category import MemberCategory

ISBN = "1234567890"


class FakeClock:
    """A clock the tests can move forward."""

    def __init__(self, today=date(2026, 1, 1)):
        self.today = today

    def __call__(self):
        return self.today

    def advance(self, days):
        """Move the clock forward by some days."""
        self.today += timedelta(days=days)


def make_library(clock=None, copies=1, category=MemberCategory.STUDENT):
    """Build a library with one book and one member."""
    library = Library(clock=clock) if clock else Library()
    library.add_book(Book(ISBN, "Clean Code", "Robert Martin", copies=copies))
    library.register_member(Member("m1", "Ana", category=category))
    return library
