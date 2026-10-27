import pytest

from book import Book
from library import Library
from member import Member

CLEAN_CODE, K_AND_R, PATTERNS = "0306406152", "0131103628", "0201633612"


@pytest.fixture(name="library")
def fixture_library(clock):
    library = Library(clock=clock)
    library.add_book(Book(CLEAN_CODE, "Clean Code", "Robert Martin", total_copies=2))
    library.add_book(Book(K_AND_R, "The C Programming Language", "Brian Kernighan", total_copies=2))
    library.add_book(Book(PATTERNS, "Design Patterns", "Erich Gamma", total_copies=2))
    library.register_member(Member("M001", "Ada Lovelace"))
    library.register_member(Member("M002", "Grace Hopper"))
    return library


def test_member_history_lists_the_members_loans_in_borrow_order(library, clock):
    library.borrow_book("M001", K_AND_R)
    library.borrow_book("M002", PATTERNS)
    clock.advance(3)
    library.return_book("M001", K_AND_R)
    library.borrow_book("M001", CLEAN_CODE)

    history = library.member_history("M001")

    assert [(loan.isbn, loan.returned_on is not None) for loan in history] == [(K_AND_R, True), (CLEAN_CODE, False)]


def test_history_of_an_unknown_member_is_rejected(library):
    with pytest.raises(LookupError, match="No member with id M404"):
        library.member_history("M404")
