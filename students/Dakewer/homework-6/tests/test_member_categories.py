from datetime import date

import pytest

from src.book import Book
from src.library import Library
from src.member import Member


def test_faculty_member_can_borrow_five_books():
    assert Member("F001", "Prof", category="faculty").max_borrow_limit == 5


def test_public_member_can_borrow_two_books():
    assert Member("P001", "Visitor", category="public").max_borrow_limit == 2


def test_unknown_category_is_rejected():
    with pytest.raises(ValueError, match="Unknown category"):
        Member("X001", "Nobody", category="alien")


@pytest.mark.parametrize(
    "category, rate",
    [("student", 1.0), ("faculty", 0.5), ("public", 2.0)],
)
def test_each_category_has_its_own_late_fee_rate(category, rate):
    assert Member("M001", "Someone", category=category).late_fee_rate == rate


def test_library_charges_late_fees_using_member_rate():
    library = Library()
    library.add_book(Book("1234567890", "A", "Author"))
    library.add_book(Book("0987654321", "B", "Author"))
    library.register_member(Member("F001", "Prof", category="faculty"))
    library.borrow_book("F001", "1234567890", borrow_date=date(2026, 1, 1))
    library.borrow_book("F001", "0987654321", borrow_date=date(2026, 1, 3))
    assert library.calculate_late_fee("F001", as_of=date(2026, 1, 20)) == 4.0


def test_library_enforces_category_borrow_limit():
    library = Library()
    for isbn in ("1234567890", "0987654321", "1111111111"):
        library.add_book(Book(isbn, "Title", "Author"))
    library.register_member(Member("P001", "Visitor", category="public"))
    library.borrow_book("P001", "1234567890")
    library.borrow_book("P001", "0987654321")
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("P001", "1111111111")
