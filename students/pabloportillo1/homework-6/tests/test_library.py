import pytest

from book import Book
from library import Library


@pytest.fixture(name="library")
def fixture_library():
    return Library()


def test_added_book_can_be_looked_up_by_isbn(library):
    book = Book("0306406152", "Clean Code", "Robert Martin")

    library.add_book(book)

    assert library.get_book("0306406152") is book
