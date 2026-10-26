import pytest
from src.book import Book
from src.member import Member
from src.library import Library


def test_library_can_be_initialized_empty():
    library = Library()
    assert len(library.books) == 0
    assert len(library.members) == 0


def test_library_add_book_success():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin")
    library.add_book(book)
    assert library.get_book("1234567890") == book


def test_library_add_book_duplicate_raises():
    library = Library()
    book1 = Book("1234567890", "Clean Code", "Robert C. Martin")
    book2 = Book("1234567890", "Clean Code", "Robert C. Martin")
    library.add_book(book1)
    with pytest.raises(ValueError, match="Book already exists in catalog"):
        library.add_book(book2)


def test_library_get_book_not_found():
    library = Library()
    with pytest.raises(KeyError, match="Book not found in catalog"):
        library.get_book("0000000000")
