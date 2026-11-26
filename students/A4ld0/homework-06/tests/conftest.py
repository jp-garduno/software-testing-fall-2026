import pytest
from src.book import Book
from src.member import Member
from src.library import Library


@pytest.fixture
def library():
    result = Library()
    result.add_book(Book("1234567890", "Dune", "Frank Herbert", 2))
    result.register_member(Member("m1", "Ana"))
    return result
