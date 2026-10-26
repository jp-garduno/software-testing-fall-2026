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


@pytest.mark.parametrize("day, fee", [(1, 0), (14, 0), (15, 0), (16, 1)])
def test_late_fees_at_due_date_boundaries(library, day, fee):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    assert library.calculate_late_fees("m1", as_of=date(2026, 10, day)) == fee


def test_returning_one_of_two_copies_closes_only_the_first_loan(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 2))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 17))
    assert library.calculate_late_fees("m1", as_of=date(2026, 10, 20)) == 6


def test_returning_and_reborrowing_creates_a_new_history_entry(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 17))
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 18))
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 19))
    assert [loan["returned_on"] for loan in library.member_history("m1")] == [
        date(2026, 10, 17), date(2026, 10, 19)]


def test_member_history_is_a_snapshot(library):
    library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
    snapshot = library.member_history("m1")
    snapshot[0]["isbn"] = "0000000000"
    library.return_book("m1", "1234567890", returned_on=date(2026, 10, 2))
    assert (library.loans[0]["isbn"], snapshot[0]["returned_on"]) == ("1234567890", None)


