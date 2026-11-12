from datetime import date, timedelta

import pytest

from book import Book
from library import Library
from member import Member


class FakeClock:
    """Controllable replacement for date.today so tests never wait for real days."""

    def __init__(self, today):
        self.today = today

    def __call__(self):
        return self.today

    def advance(self, days):
        self.today += timedelta(days=days)


@pytest.fixture
def clock():
    return FakeClock(date(2026, 10, 1))


@pytest.fixture
def library(clock):
    lib = Library(clock=clock)
    lib.add_book(Book("0306406152", "Clean Code", "Robert C. Martin", total_copies=2))
    lib.register_member(Member("M001", "Ana Lopez"))
    return lib
