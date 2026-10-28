import pytest
from src.book import Book
from src.member import Member
from src.library import Library


def test_library_creation():
    lib = Library()
    assert lib.books == {}
    assert lib.members == {}


def test_library_add_book_success():
    lib = Library()
    book = Book("1234567890", "Design Patterns", "Gang of Four", total_copies=3)
    lib.add_book(book)
    assert "1234567890" in lib.books
    assert lib.books["1234567890"].title == "Design Patterns"


def test_library_add_book_increments_existing_copies():
    lib = Library()
    book1 = Book("1234567890", "Design Patterns", "Gang of Four", total_copies=2)
    book2 = Book("1234567890", "Design Patterns", "Gang of Four", total_copies=3)
    lib.add_book(book1)
    lib.add_book(book2)
    assert lib.books["1234567890"].total_copies == 5
    assert lib.books["1234567890"].available_copies == 5


def test_library_add_book_rejects_invalid_type():
    lib = Library()
    with pytest.raises(TypeError, match="Expected Book instance"):
        lib.add_book("not a book")


def test_library_register_member_success():
    lib = Library()
    member = Member("M001", "Alice")
    lib.register_member(member)
    assert "M001" in lib.members
    assert lib.members["M001"].name == "Alice"


def test_library_register_member_rejects_duplicate():
    lib = Library()
    member1 = Member("M001", "Alice")
    member2 = Member("M001", "Alice Duplicate")
    lib.register_member(member1)
    with pytest.raises(ValueError, match="Member with this ID already registered"):
        lib.register_member(member2)


def test_library_register_member_rejects_invalid_type():
    lib = Library()
    with pytest.raises(TypeError, match="Expected Member instance"):
        lib.register_member("not a member")
