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


def test_library_borrow_book_success():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=2)
    member = Member("M001", "Alice Smith")
    library.add_book(book)
    library.register_member(member)

    library.borrow_book("M001", "1234567890")

    assert book.available_copies == 1
    assert "1234567890" in member.borrowed_books


def test_library_borrow_book_unavailable_raises():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=1)
    member1 = Member("M001", "Alice")
    member2 = Member("M002", "Bob")
    library.add_book(book)
    library.register_member(member1)
    library.register_member(member2)

    library.borrow_book("M001", "1234567890")
    with pytest.raises(RuntimeError, match="No copies available"):
        library.borrow_book("M002", "1234567890")


def test_library_borrow_book_limit_reached_raises():
    library = Library()
    book1 = Book("1111111111", "Book 1", "Author 1")
    book2 = Book("2222222222", "Book 2", "Author 2")
    member = Member("M001", "Alice", max_borrow_limit=1)
    library.add_book(book1)
    library.add_book(book2)
    library.register_member(member)

    library.borrow_book("M001", "1111111111")
    with pytest.raises(ValueError, match="Borrow limit reached"):
        library.borrow_book("M001", "2222222222")


def test_library_borrow_book_member_not_found():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin")
    library.add_book(book)
    with pytest.raises(KeyError, match="Member not found"):
        library.borrow_book("M999", "1234567890")


def test_library_borrow_book_book_not_found():
    library = Library()
    member = Member("M001", "Alice")
    library.register_member(member)
    with pytest.raises(KeyError, match="Book not found"):
        library.borrow_book("M001", "9999999999")


def test_library_return_book_success():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=1)
    member = Member("M001", "Alice Smith")
    library.add_book(book)
    library.register_member(member)

    library.borrow_book("M001", "1234567890")
    assert book.available_copies == 0

    fee = library.return_book("M001", "1234567890")
    assert fee == 0.0
    assert book.available_copies == 1
    assert "1234567890" not in member.borrowed_books
    assert len(library.active_loans) == 0
    assert len(library.loan_history) == 1


def test_library_return_book_not_borrowed_by_member():
    library = Library()
    book = Book("1234567890", "Clean Code", "Robert C. Martin", total_copies=1)
    member = Member("M001", "Alice Smith")
    library.add_book(book)
    library.register_member(member)

    with pytest.raises(ValueError, match="Book was not borrowed by this member"):
        library.return_book("M001", "1234567890")
