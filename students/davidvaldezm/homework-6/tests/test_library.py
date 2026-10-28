import pytest

from src.library import Library

from src.book import Book
from src.member import Member


@pytest.fixture
def library():
    catalog = Library()
    catalog.add_book(Book("1234567890", "Pedro Paramo", "Juan Rulfo", 2))
    catalog.add_book(Book("1234567890123", "El llano en llamas", "Juan Rulfo", 0))
    catalog.register_member(Member("M1", "Ana"))
    return catalog


def test_library_starts_with_empty_catalog_and_members():
    catalog = Library()
    assert (catalog.catalog, catalog.members) == ({}, {})
