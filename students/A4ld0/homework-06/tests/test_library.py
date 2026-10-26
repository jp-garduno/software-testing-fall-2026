import pytest
from src.book import Book
from src.member import Member
from src.library import Library


def test_library_starts_empty():
    library = Library()
    assert (library.catalog, library.members) == ({}, {})


def test_add_book():
    library = Library()
    book = Book("1234567890", "Dune", "Frank Herbert")
    library.add_book(book)
    assert library.catalog[book.isbn] is book


def test_duplicate_isbn_preserves_catalog():
    library = Library()
    original = Book("1234567890", "Dune", "Frank Herbert")
    library.add_book(original)
    with pytest.raises(ValueError, match="ISBN"):
        library.add_book(Book(original.isbn, "Replacement", "Other"))
    assert library.catalog[original.isbn] is original


def test_register_member():
    library = Library()
    member = Member("m1", "Ana")
    library.register_member(member)
    assert library.members[member.member_id] is member


def test_duplicate_member_preserves_registration():
    library = Library()
    original = Member("m1", "Ana")
    library.register_member(original)
    with pytest.raises(ValueError, match="member"):
        library.register_member(Member("m1", "Other"))
    assert library.members["m1"] is original


@pytest.fixture
def library():
    result = Library()
    result.add_book(Book("1234567890", "Dune", "Frank Herbert", 2))
    result.register_member(Member("m1", "Ana"))
    return result


def test_library_borrow_updates_book_and_member(library):
    library.borrow_book("m1", "1234567890")
    assert (library.catalog["1234567890"].available_copies,
            library.members["m1"].borrowed_books) == (1, ["1234567890"])


def test_borrow_unknown_member(library):
    with pytest.raises(ValueError, match="member"):
        library.borrow_book("missing", "1234567890")
    assert library.catalog["1234567890"].available_copies == 2


def test_borrow_unknown_isbn(library):
    with pytest.raises(ValueError, match="ISBN"):
        library.borrow_book("m1", "0000000000")
    assert library.members["m1"].borrowed_books == []


def test_borrow_limit_is_atomic(library):
    library.members["m1"].max_borrow_limit = 0
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("m1", "1234567890")
    assert (library.catalog["1234567890"].available_copies,
            library.members["m1"].borrowed_books) == (2, [])


def test_library_return_updates_book_and_member(library):
    library.borrow_book("m1", "1234567890")
    library.return_book("m1", "1234567890")
    assert (library.catalog["1234567890"].available_copies,
            library.members["m1"].borrowed_books) == (2, [])


def test_search_by_title(library):
    library.add_book(Book("1234567890123", "Dune Messiah", "Frank Herbert"))
    assert [book.title for book in library.search_by_title("DUNE")] == ["Dune", "Dune Messiah"]
