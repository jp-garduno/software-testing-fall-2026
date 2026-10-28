from datetime import date
import pytest
from src.book import Book
from src.member import Member
from src.library import Library

def make_book(isbn="1234567890", copies=1, title="Clean Code", author="Robert Martin"):
    return Book(isbn, title, author, copies=copies)

@pytest.fixture
def library():
    return Library()

def test_added_book_appears_in_available_books(library):
    book = make_book()
    library.add_book(book)
    assert library.get_available_books() == [book]

def test_available_books_excludes_books_without_copies(library):
    library.add_book(make_book("1234567890", copies=0))
    assert library.get_available_books() == []

def test_add_duplicate_isbn_raises(library):
    library.add_book(make_book())
    with pytest.raises(ValueError, match="already"):
        library.add_book(make_book())

def test_register_member_can_be_retrieved(library):
    m = Member("m1", "Ana")
    library.register_member(m)
    assert library.get_member("m1") is m

def test_register_duplicate_member_raises(library):
    library.register_member(Member("m1", "Ana"))
    with pytest.raises(ValueError, match="already"):
        library.register_member(Member("m1", "Otra"))

@pytest.fixture
def loaded(library):
    book = make_book(copies=2)
    member = Member("m1", "Ana")
    library.add_book(book)
    library.register_member(member)
    return library, book, member

def test_borrow_book_updates_book_and_member(loaded):
    lib, book, member = loaded
    lib.borrow_book("m1", "1234567890")
    assert book.available_copies == 1
    assert member.borrowed_books == ["1234567890"]

def test_borrow_unknown_member_raises(loaded):
    lib, _, _ = loaded
    with pytest.raises(ValueError, match="Member not found"):
        lib.borrow_book("ghost", "1234567890")

def test_borrow_unknown_book_raises(loaded):
    lib, _, _ = loaded
    with pytest.raises(ValueError, match="Book not found"):
        lib.borrow_book("m1", "0000000000")

def test_borrow_at_member_limit_fails_and_keeps_copies(library):
    b1, b2 = make_book("1234567890"), make_book("1234567891", copies=2)
    library.add_book(b1)
    library.add_book(b2)
    library.register_member(Member("m1", "Ana", max_borrow_limit=1))
    library.borrow_book("m1", "1234567890")
    with pytest.raises(ValueError):
        library.borrow_book("m1", "1234567891")
    assert b2.available_copies == 2

def test_member_cannot_borrow_same_book_twice(loaded):
    lib, _, _ = loaded
    lib.borrow_book("m1", "1234567890")
    with pytest.raises(ValueError, match="already borrowed"):
        lib.borrow_book("m1", "1234567890")

def test_return_book_restores_copy_and_clears_member(loaded):
    lib, book, member = loaded
    lib.borrow_book("m1", "1234567890")
    lib.return_book("m1", "1234567890")
    assert book.available_copies == 2
    assert member.borrowed_books == []

def test_return_unknown_member_raises(loaded):
    lib, _, _ = loaded
    with pytest.raises(ValueError, match="Member not found"):
        lib.return_book("ghost", "1234567890")

def test_search_by_title_is_partial_and_case_insensitive(library):
    clean = make_book("1234567890", title="Clean Code")
    other = make_book("1234567891", title="The Pragmatic Programmer")
    library.add_book(clean)
    library.add_book(other)
    assert library.search_by_title("clean") == [clean]

def test_search_by_author(library):
    b = make_book(author="Robert Martin")
    library.add_book(b)
    assert library.search_by_author("martin") == [b]

def test_no_late_fee_without_loans(loaded):
    lib, _, _ = loaded
    assert lib.calculate_late_fees("m1", today=date(2026, 1, 20)) == 0
