import pytest

from book import Book
from library import Library
from member import Member


@pytest.fixture(name="library")
def fixture_library():
    return Library()


@pytest.fixture(name="book")
def fixture_book(library):
    book = Book("0306406152", "Clean Code", "Robert Martin", total_copies=2)
    library.add_book(book)
    return book


@pytest.fixture(name="member")
def fixture_member(library):
    member = Member("M001", "Ada Lovelace")
    library.register_member(member)
    return member


def test_added_book_can_be_looked_up_by_isbn(library):
    book = Book("0306406152", "Clean Code", "Robert Martin")

    library.add_book(book)

    assert library.get_book("0306406152") is book


def test_adding_a_book_with_an_existing_isbn_is_rejected(library):
    library.add_book(Book("0306406152", "Clean Code", "Robert Martin"))

    with pytest.raises(ValueError, match="already in the catalog"):
        library.add_book(Book("0306406152", "Another Title", "Someone Else"))


def test_registered_member_can_be_looked_up_by_id(library):
    member = Member("M001", "Ada Lovelace")

    library.register_member(member)

    assert library.get_member("M001") is member


def test_registering_an_existing_member_id_is_rejected(library):
    library.register_member(Member("M001", "Ada Lovelace"))

    with pytest.raises(ValueError, match="already registered"):
        library.register_member(Member("M001", "Grace Hopper"))


def test_looking_up_an_unknown_isbn_is_rejected(library):
    with pytest.raises(LookupError, match="No book with ISBN 0306406152"):
        library.get_book("0306406152")


def test_looking_up_an_unknown_member_is_rejected(library):
    with pytest.raises(LookupError, match="No member with id M404"):
        library.get_member("M404")


def test_borrow_book_takes_a_copy_and_records_it_on_the_member(library, book, member):
    library.borrow_book("M001", "0306406152")

    assert (book.available_copies, member.borrowed_books) == (1, ["0306406152"])


def test_borrowing_an_unavailable_book_leaves_the_member_unchanged(library, book, member):
    book.borrow()
    book.borrow()

    with pytest.raises(ValueError, match="No copies available"):
        library.borrow_book("M001", "0306406152")
    assert member.borrowed_books == []


def test_borrowing_beyond_the_member_limit_leaves_the_copies_unchanged(library, book, member):
    for isbn in ("0131103628", "0201633612", "0596007124"):
        library.add_book(Book(isbn, f"Book {isbn}", "Author"))
        library.borrow_book("M001", isbn)

    with pytest.raises(ValueError, match="borrow limit"):
        library.borrow_book("M001", "0306406152")
    assert book.available_copies == 2
