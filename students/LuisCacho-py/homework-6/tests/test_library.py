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


def test_library_register_member_success():
    library = Library()
    member = Member("M001", "Alice Smith")
    library.register_member(member)
    assert library.get_member("M001") == member


def test_library_register_member_duplicate_raises():
    library = Library()
    member1 = Member("M001", "Alice Smith")
    member2 = Member("M001", "Alice Clone")
    library.register_member(member1)
    with pytest.raises(ValueError, match="Member already registered"):
        library.register_member(member2)


def test_library_get_member_not_found():
    library = Library()
    with pytest.raises(KeyError, match="Member not found"):
        library.get_member("M999")
