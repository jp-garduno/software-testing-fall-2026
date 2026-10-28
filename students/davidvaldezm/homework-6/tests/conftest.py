"""Fresh in-memory libraries and deterministic clocks for every test."""

from datetime import date

import pytest

from src.book import Book
from src.library import Library
from src.member import Member


@pytest.fixture
def library():
    """Provide isolated domain objects for each requesting test."""
    catalog = Library()
    catalog.add_book(Book("1234567890", "Pedro Paramo", "Juan Rulfo", 2))
    catalog.add_book(Book("1234567890123", "El llano en llamas", "Juan Rulfo", 0))
    catalog.register_member(Member("M1", "Ana"))
    return catalog


@pytest.fixture
def dated_library():
    """Provide isolated domain objects for each requesting test."""
    clock = [date(2026, 1, 1)]
    catalog = Library(today=lambda: clock[0])
    catalog.add_book(Book("1234567890", "Title", "Author", 2))
    catalog.register_member(Member("M1", "Ana"))
    return catalog, clock
