import pytest
from src.book import Book
from src.member import Member
from src.library import Library


def test_library_starts_empty():
    library = Library()
    assert (library.catalog, library.members) == ({}, {})
