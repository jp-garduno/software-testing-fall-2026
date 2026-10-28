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


def test_library_borrow_book_success():
    lib = Library()
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=2)
    member = Member("M001", "Alice")
    lib.add_book(book)
    lib.register_member(member)

    assert lib.borrow_book("M001", "1234567890") is True
    assert book.available_copies == 1
    assert "1234567890" in member.borrowed_books


def test_library_borrow_book_raises_for_unregistered_member():
    lib = Library()
    book = Book("1234567890", "Refactoring", "Martin Fowler")
    lib.add_book(book)
    with pytest.raises(KeyError, match="Member not registered"):
        lib.borrow_book("UNKNOWN", "1234567890")


def test_library_borrow_book_raises_for_missing_book():
    lib = Library()
    member = Member("M001", "Alice")
    lib.register_member(member)
    with pytest.raises(KeyError, match="Book not found in catalog"):
        lib.borrow_book("M001", "9999999999")


def test_library_borrow_book_raises_when_unavailable():
    lib = Library()
    book = Book("1234567890", "Refactoring", "Martin Fowler", total_copies=1)
    member1 = Member("M001", "Alice")
    member2 = Member("M002", "Bob")
    lib.add_book(book)
    lib.register_member(member1)
    lib.register_member(member2)

    lib.borrow_book("M001", "1234567890")
    with pytest.raises(ValueError, match="Book is not currently available"):
        lib.borrow_book("M002", "1234567890")


def test_library_borrow_book_raises_when_member_limit_reached():
    lib = Library()
    book1 = Book("1111111111", "Book 1", "Author")
    book2 = Book("2222222222", "Book 2", "Author")
    member = Member("M001", "Alice", max_borrow_limit=1)
    lib.add_book(book1)
    lib.add_book(book2)
    lib.register_member(member)

    lib.borrow_book("M001", "1111111111")
    with pytest.raises(ValueError, match="Borrow limit reached"):
        lib.borrow_book("M001", "2222222222")
