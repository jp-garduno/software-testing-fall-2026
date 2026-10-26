"""Cross-feature regressions and boundary conditions after the TDD cycles."""
from datetime import date

import pytest

from src.book import Book
from src.member import Member


def test_wrong_member_cannot_return_someone_elses_book(library):
    library.register_member(Member("m2", "Luis"))
    library.borrow_book("m1", "1234567890")
    with pytest.raises(ValueError, match="not borrowed"):
        library.return_book("m2", "1234567890")
    assert (library.catalog["1234567890"].available_copies,
            library.members["m1"].borrowed_books) == (1, ["1234567890"])


def test_unavailable_book_does_not_create_a_phantom_loan(library):
    library.borrow_book("m1", "1234567890")
    library.borrow_book("m1", "1234567890")
    with pytest.raises(ValueError, match="available"):
        library.borrow_book("m1", "1234567890")
    assert (len(library.loans), len(library.members["m1"].borrowed_books)) == (2, 2)


