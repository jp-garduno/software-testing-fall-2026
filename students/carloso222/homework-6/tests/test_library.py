import pytest

from src.book import Book
from src.exceptions import (
    AlreadyBorrowedError,
    BookNotBorrowedError,
    BookNotFoundError,
    BorrowLimitReachedError,
    DuplicateBookError,
    DuplicateMemberError,
    MemberNotFoundError,
    NoCopiesAvailableError,
)
from src.library import Library
from src.member import Member
from tests.conftest import CLEAN_CODE, REFACTORING, START_DATE, TDD_BY_EXAMPLE


def test_added_book_can_be_found_by_isbn():
    library = Library()
    book = Book("1234567890", "Test Book", "Author")
    library.add_book(book)
    assert library.get_book("1234567890") is book


def test_adding_a_duplicate_isbn_raises():
    library = Library()
    library.add_book(Book("1234567890", "Test Book", "Author"))
    with pytest.raises(DuplicateBookError):
        library.add_book(Book("1234567890", "Other", "Author"))


def test_get_book_raises_for_unknown_isbn():
    with pytest.raises(BookNotFoundError):
        Library().get_book("0000000000")


def test_registered_member_can_be_found_by_id():
    library = Library()
    member = Member("M1", "Ana")
    library.register_member(member)
    assert library.get_member("M1") is member


def test_registering_a_duplicate_member_id_raises():
    library = Library()
    library.register_member(Member("M1", "Ana"))
    with pytest.raises(DuplicateMemberError):
        library.register_member(Member("M1", "Otra Ana"))


def test_get_member_raises_for_unknown_id():
    with pytest.raises(MemberNotFoundError):
        Library().get_member("X")


def test_library_uses_todays_date_by_default():
    library = Library()
    library.add_book(Book("1234567890", "Test Book", "Author"))
    library.register_member(Member("M1", "Ana"))
    loan = library.borrow_book("M1", "1234567890")
    assert loan.borrowed_on is not None


def test_borrow_book_takes_a_copy_off_the_shelf(library):
    library.borrow_book("S1", CLEAN_CODE)
    assert library.get_book(CLEAN_CODE).available_copies == 1


def test_borrow_book_records_the_book_on_the_member(library):
    library.borrow_book("S1", CLEAN_CODE)
    assert library.get_member("S1").borrowed_books == [CLEAN_CODE]


def test_borrow_book_returns_a_loan_dated_today(library):
    loan = library.borrow_book("S1", CLEAN_CODE)
    assert (loan.member_id, loan.isbn, loan.borrowed_on) == ("S1", CLEAN_CODE, START_DATE)


def test_borrow_book_raises_for_unknown_member(library):
    with pytest.raises(MemberNotFoundError):
        library.borrow_book("NOPE", CLEAN_CODE)


def test_borrow_book_raises_for_unknown_isbn(library):
    with pytest.raises(BookNotFoundError):
        library.borrow_book("S1", "0000000000")


def test_borrow_book_raises_when_no_copies_left(library):
    library.borrow_book("S1", REFACTORING)
    with pytest.raises(NoCopiesAvailableError):
        library.borrow_book("S2", REFACTORING)


def test_member_cannot_borrow_two_copies_of_the_same_book(library):
    library.borrow_book("S1", CLEAN_CODE)
    with pytest.raises(AlreadyBorrowedError):
        library.borrow_book("S1", CLEAN_CODE)


def test_borrow_book_respects_member_limit(library):
    library.add_book(Book("1111111111", "Extra", "Author"))
    for isbn in (CLEAN_CODE, REFACTORING, TDD_BY_EXAMPLE):
        library.borrow_book("S1", isbn)
    with pytest.raises(BorrowLimitReachedError):
        library.borrow_book("S1", "1111111111")


def test_failed_borrow_over_limit_leaves_book_on_shelf(library):
    library.register_member(Member("Z1", "Zoe", max_borrow_limit=0))
    with pytest.raises(BorrowLimitReachedError):
        library.borrow_book("Z1", CLEAN_CODE)
    assert library.get_book(CLEAN_CODE).available_copies == 2


def test_return_book_puts_the_copy_back(library):
    library.borrow_book("S1", REFACTORING)
    library.return_book("S1", REFACTORING)
    assert library.get_book(REFACTORING).is_available() is True


def test_return_book_removes_book_from_member(library):
    library.borrow_book("S1", REFACTORING)
    library.return_book("S1", REFACTORING)
    assert library.get_member("S1").borrowed_books == []


def test_return_book_raises_when_member_did_not_borrow_it(library):
    with pytest.raises(BookNotBorrowedError):
        library.return_book("S1", REFACTORING)


def test_return_book_raises_for_unknown_member(library):
    with pytest.raises(MemberNotFoundError):
        library.return_book("NOPE", REFACTORING)
