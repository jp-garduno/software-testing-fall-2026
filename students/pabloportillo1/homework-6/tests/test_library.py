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


def test_adding_a_book_with_an_existing_isbn_is_rejected(library):
    library.add_book(Book("0306406152", "Clean Code", "Robert Martin"))

    with pytest.raises(ValueError, match="already in the catalog"):
        library.add_book(Book("0306406152", "Another Title", "Someone Else"))
