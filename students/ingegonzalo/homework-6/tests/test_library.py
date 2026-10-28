import pytest

from src.book import Book
from src.library import Library
from src.member import Member

def test_new_library_has_no_available_books():
    library = Library()
    assert library.get_available_books() == []

def test_add_book_makes_it_available_in_catalog():
    library = Library()
    book = Book("1234567890", "Test Book", "Author")
    library.add_book(book)
    assert library.get_available_books() == [book]

def test_get_available_books_excludes_books_without_copies():
    library = Library()
    available = Book("1111111111", "Available", "Author", total_copies=1)
    unavailable = Book("2222222222", "Unavailable", "Author", total_copies=0)
    library.add_book(available)
    library.add_book(unavailable)
    assert library.get_available_books() == [available]

def test_add_book_rejects_duplicate_isbn():
    library = Library()
    library.add_book(Book("1234567890", "Test Book", "Author"))
    with pytest.raises(ValueError):
        library.add_book(Book("1234567890", "Another Book", "Author"))

def test_register_member_makes_member_retrievable():
    library = Library()
    member = Member("M001", "Ana")
    library.register_member(member)
    assert library.get_member("M001") is member

def test_get_member_raises_error_when_not_registered():
    library = Library()
    with pytest.raises(ValueError, match="not registered"):
        library.get_member("M999")