import pytest

from src.book import Book
from src.library import Library
from src.member import Member

def test_new_library_has_no_available_books():
    library = Library()
    assert library.get_available_books() == []
    