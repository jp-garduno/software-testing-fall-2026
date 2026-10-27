import pytest
from library import Library
from book import Book
from member import Member

def test_library_add_book():
    lib = Library()
    book = Book("1234567890", "TDD", "Author")
    lib.add_book(book)
    assert "1234567890" in lib.catalog

def test_library_register_member():
    lib = Library()
    member = Member(1, "Alice")
    lib.register_member(member)
    assert 1 in lib.members

def test_borrow_book_success():
    lib = Library()
    lib.add_book(Book("1234567890", "TDD", "Author", 1))
    lib.register_member(Member(1, "Alice"))
    lib.borrow_book(1, "1234567890")
    assert lib.catalog["1234567890"].available_copies == 0
    assert "1234567890" in lib.members[1].borrowed_books

def test_borrow_book_not_found():
    lib = Library()
    with pytest.raises(ValueError, match="Member or Book not found"):
        lib.borrow_book(1, "1234567890")

def test_return_book_with_fees():
    lib = Library()
    lib.add_book(Book("1234567890", "TDD", "Author", 1))
    lib.register_member(Member(1, "Alice"))
    lib.borrow_book(1, "1234567890")
    lib.return_book(1, "1234567890", days_borrowed=15)
    assert lib.catalog["1234567890"].available_copies == 1
    assert lib.members[1].late_fees == 1.0

def test_search_books():
    lib = Library()
    lib.add_book(Book("1111111111", "TDD Python", "Alice"))
    lib.add_book(Book("2222222222", "TDD JS", "Bob"))
    results = lib.search_books(title="python")
    assert len(results) == 1
    assert results[0].isbn == "1111111111"

def test_get_available_books():
    lib = Library()
    lib.add_book(Book("1111111111", "A", "A", 1))
    lib.add_book(Book("2222222222", "B", "B", 0))
    assert len(lib.get_available_books()) == 1