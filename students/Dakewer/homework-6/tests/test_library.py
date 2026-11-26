import pytest

from src.book import Book
from src.library import Library
from src.member import Member


@pytest.fixture
def library():
    return Library()


@pytest.fixture
def book():
    return Book("1234567890", "Clean Code", "Robert Martin", copies=2)


@pytest.fixture
def member():
    return Member("M001", "Alice")


def test_library_can_add_book_to_catalog(library, book):
    library.add_book(book)
    assert library.get_book("1234567890") is book


def test_library_rejects_duplicate_isbn(library, book):
    library.add_book(book)
    with pytest.raises(ValueError, match="already in catalog"):
        library.add_book(Book("1234567890", "Other", "Someone"))


def test_library_can_register_member(library, member):
    library.register_member(member)
    assert library.get_member("M001") is member


def test_library_rejects_duplicate_member(library, member):
    library.register_member(member)
    with pytest.raises(ValueError, match="already registered"):
        library.register_member(Member("M001", "Bob"))


def test_borrow_book_gives_book_to_member_and_reduces_copies(library, book, member):
    library.add_book(book)
    library.register_member(member)
    library.borrow_book("M001", "1234567890")
    assert member.borrowed_books == ["1234567890"]
    assert book.available_copies == 1


def test_borrow_book_fails_for_unknown_member(library, book):
    library.add_book(book)
    with pytest.raises(ValueError, match="Unknown member"):
        library.borrow_book("NOPE", "1234567890")


def test_borrow_book_fails_for_unknown_book(library, member):
    library.register_member(member)
    with pytest.raises(ValueError, match="Unknown book"):
        library.borrow_book("M001", "9999999999")


def test_failed_borrow_at_limit_does_not_take_a_copy(library):
    library.add_book(Book("1234567890", "A", "Author", copies=2))
    library.add_book(Book("0987654321", "B", "Author", copies=2))
    library.register_member(Member("M001", "Alice", max_borrow_limit=1))
    library.borrow_book("M001", "1234567890")
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("M001", "0987654321")
    assert library.get_book("0987654321").available_copies == 2


def test_failed_borrow_of_unavailable_book_leaves_member_untouched(library, member):
    library.add_book(Book("1234567890", "Rare", "Author", copies=0))
    library.register_member(member)
    with pytest.raises(ValueError, match="No copies"):
        library.borrow_book("M001", "1234567890")
    assert member.borrowed_books == []


def test_return_book_gives_copy_back_and_clears_member_loan(library, book, member):
    library.add_book(book)
    library.register_member(member)
    library.borrow_book("M001", "1234567890")
    library.return_book("M001", "1234567890")
    assert member.borrowed_books == []
    assert book.available_copies == 2


def test_return_book_fails_for_unknown_member(library, book):
    library.add_book(book)
    with pytest.raises(ValueError, match="Unknown member"):
        library.return_book("NOPE", "1234567890")


def test_return_book_fails_for_unknown_book(library, member):
    library.register_member(member)
    with pytest.raises(ValueError, match="Unknown book"):
        library.return_book("M001", "9999999999")


def test_search_by_title_finds_partial_case_insensitive_match(library, book):
    library.add_book(book)
    assert library.search_by_title("clean") == [book]


def test_search_by_author_finds_partial_case_insensitive_match(library, book):
    library.add_book(book)
    library.add_book(Book("0987654321", "Refactoring", "Martin Fowler"))
    assert library.search_by_author("fowler") == [library.get_book("0987654321")]


def test_search_with_blank_query_is_rejected(library):
    with pytest.raises(ValueError, match="empty"):
        library.search_by_title("  ")


def test_get_available_books_excludes_books_without_copies(library, book):
    library.add_book(book)
    library.add_book(Book("0987654321", "Out Of Stock", "Author", copies=0))
    assert library.get_available_books() == [book]
