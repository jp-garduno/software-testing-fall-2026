import pytest

from book import Book
from library import Library
from member import Member

ISBN = "1234567890"
OTHER_ISBN = "0987654321"


@pytest.fixture
def library():
    return Library()


def test_added_book_is_listed_as_available(library):
    book = Book(ISBN, "Test Book", "Author")
    library.add_book(book)
    assert library.get_available_books() == [book]


def test_available_books_excludes_books_without_copies(library):
    available = Book(ISBN, "Available", "Author", copies=1)
    gone = Book(OTHER_ISBN, "Gone", "Author", copies=0)
    library.add_book(available)
    library.add_book(gone)
    assert library.get_available_books() == [available]


def test_registered_member_can_be_found(library):
    member = Member("m1", "Alice")
    library.register_member(member)
    assert library.get_member("m1") is member


def test_borrow_book_takes_a_copy(library):
    book = Book(ISBN, "Test Book", "Author", copies=1)
    library.add_book(book)
    library.register_member(Member("m1", "Alice"))
    library.borrow_book("m1", ISBN)
    assert book.available_copies == 0


def test_borrow_book_fails_for_unknown_member(library):
    library.add_book(Book(ISBN, "Test Book", "Author"))
    with pytest.raises(ValueError, match="Member not found"):
        library.borrow_book("ghost", ISBN)


def test_borrow_book_fails_for_unknown_book(library):
    library.register_member(Member("m1", "Alice"))
    with pytest.raises(ValueError, match="Book not found"):
        library.borrow_book("m1", ISBN)


def test_borrow_over_the_limit_does_not_take_a_copy(library):
    first = Book(ISBN, "First", "Author", copies=1)
    second = Book(OTHER_ISBN, "Second", "Author", copies=2)
    library.add_book(first)
    library.add_book(second)
    library.register_member(Member("m1", "Alice", max_borrow_limit=1))
    library.borrow_book("m1", ISBN)
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("m1", OTHER_ISBN)
    assert second.available_copies == 2


def test_borrowing_an_unavailable_book_leaves_member_unchanged(library):
    library.add_book(Book(ISBN, "Empty", "Author", copies=0))
    member = Member("m1", "Alice")
    library.register_member(member)
    with pytest.raises(ValueError, match="No copies available"):
        library.borrow_book("m1", ISBN)
    assert member.borrowed_books == []


def test_return_book_restores_the_copy(library):
    book = Book(ISBN, "Test Book", "Author", copies=1)
    library.add_book(book)
    library.register_member(Member("m1", "Alice"))
    library.borrow_book("m1", ISBN)
    library.return_book("m1", ISBN)
    assert book.available_copies == 1


def test_returning_a_book_you_never_borrowed_leaves_stock_unchanged(library):
    book = Book(ISBN, "Test Book", "Author", copies=2)
    library.add_book(book)
    library.register_member(Member("m1", "Alice"))
    library.register_member(Member("m2", "Bob"))
    library.borrow_book("m1", ISBN)
    with pytest.raises(ValueError, match="not borrowed"):
        library.return_book("m2", ISBN)
    assert book.available_copies == 1


def test_search_by_title_matches_partial_text_ignoring_case(library):
    match = Book(ISBN, "The Pragmatic Programmer", "Hunt")
    library.add_book(match)
    library.add_book(Book(OTHER_ISBN, "Clean Code", "Martin"))
    assert library.search_by_title("pragmatic") == [match]
