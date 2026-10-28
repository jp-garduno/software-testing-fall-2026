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

def test_register_member_rejects_duplicate_id():
    library = Library()
    library.register_member(Member("M001", "Ana"))
    with pytest.raises(ValueError):
        library.register_member(Member("M001", "Beto"))

def test_borrow_book_decreases_available_copies():
    library = Library()
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    library.add_book(book)
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890")
    assert book.available_copies == 1

def test_borrow_book_adds_isbn_to_member():
    library = Library()
    library.add_book(Book("1234567890", "Test Book", "Author"))
    member = Member("M001", "Ana")
    library.register_member(member)
    library.borrow_book("M001", "1234567890")
    assert "1234567890" in member.borrowed_books

def test_borrow_book_raises_error_when_book_not_in_catalog():
    library = Library()
    library.register_member(Member("M001", "Ana"))
    with pytest.raises(ValueError, match="not in the catalog"):
        library.borrow_book("M001", "9999999999")

def test_borrow_book_does_not_consume_copy_when_member_at_limit():
    library = Library()
    first = Book("1111111111", "First", "Author")
    second = Book("2222222222", "Second", "Author")
    library.add_book(first)
    library.add_book(second)
    library.register_member(Member("M001", "Ana", max_borrow_limit=1))
    library.borrow_book("M001", "1111111111")
    with pytest.raises(ValueError):
        library.borrow_book("M001", "2222222222")
    assert second.available_copies == 1

def test_borrow_book_does_not_register_loan_when_book_unavailable():
    library = Library()
    library.add_book(Book("1234567890", "Test Book", "Author", total_copies=0))
    member = Member("M001", "Ana")
    library.register_member(member)
    with pytest.raises(ValueError):
        library.borrow_book("M001", "1234567890")
    assert member.borrowed_books == []

def test_return_book_increases_available_copies():
    library = Library()
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    library.add_book(book)
    library.register_member(Member("M001", "Ana"))
    library.borrow_book("M001", "1234567890")
    library.return_book("M001", "1234567890")
    assert book.available_copies == 2

def test_return_book_removes_isbn_from_member():
    library = Library()
    library.add_book(Book("1234567890", "Test Book", "Author"))
    member = Member("M001", "Ana")
    library.register_member(member)
    library.borrow_book("M001", "1234567890")
    library.return_book("M001", "1234567890")
    assert member.borrowed_books == []

def test_return_book_does_not_change_copies_when_member_did_not_borrow_it():
    library = Library()
    book = Book("1234567890", "Test Book", "Author", total_copies=2)
    library.add_book(book)
    library.register_member(Member("M001", "Ana"))
    library.register_member(Member("M002", "Beto"))
    library.borrow_book("M001", "1234567890")
    with pytest.raises(ValueError):
        library.return_book("M002", "1234567890")
    assert book.available_copies == 1

def test_search_by_title_finds_matching_book():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert Martin")
    library.add_book(book)
    library.add_book(Book("0987654321", "Refactoring", "Martin Fowler"))
    assert library.search_by_title("Clean Code") == [book]