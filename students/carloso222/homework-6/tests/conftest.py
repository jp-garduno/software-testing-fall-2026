"""Shared fixtures: a controllable clock and a ready-made library."""

from datetime import date, timedelta
from unittest.mock import Mock

import pytest

from src.book import Book
from src.library import Library
from src.member import Member
from src.member_category import MemberCategory

START_DATE = date(2026, 10, 1)
CLEAN_CODE = "9780132350884"
REFACTORING = "9780134757599"
TDD_BY_EXAMPLE = "0321146530"


class FakeClock:
    """A clock tests can move forward instead of waiting for real days."""

    def __init__(self, today=START_DATE):
        self.today = today

    def __call__(self):
        return self.today

    def advance(self, days):
        self.today += timedelta(days=days)


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def notifier():
    return Mock()


@pytest.fixture
def library(clock, notifier):
    lib = Library(clock=clock, notifier=notifier)
    lib.add_book(
        Book(CLEAN_CODE, "Clean Code", "Robert C. Martin", 2,
             genre="Programming", year=2008, rating=4.4)
    )
    lib.add_book(
        Book(REFACTORING, "Refactoring", "Martin Fowler", 1,
             genre="Programming", year=2018, rating=4.7)
    )
    lib.add_book(
        Book(TDD_BY_EXAMPLE, "Test Driven Development: By Example", "Kent Beck", 1,
             genre="Testing", year=2002, rating=4.3)
    )
    lib.register_member(Member("S1", "Ana"))
    lib.register_member(Member("S2", "Luis"))
    lib.register_member(Member("F1", "Dra. Ruiz", MemberCategory.FACULTY))
    lib.register_member(Member("P1", "Jorge", MemberCategory.PUBLIC))
    return lib
