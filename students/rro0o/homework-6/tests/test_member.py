"""Tests for the Member class."""
# pylint: disable=missing-function-docstring

import pytest

from src.errors import LibraryError
from src.member import Member
from src.member_category import MemberCategory


def test_member_starts_with_id_name_no_books_and_default_limit():
    member = Member("m1", "Ana")
    assert (member.member_id, member.name, member.borrowed_books, member.max_borrow_limit) == ("m1", "Ana", [], 3)


def test_member_accepts_custom_borrow_limit():
    assert Member("m1", "Ana", max_borrow_limit=5).max_borrow_limit == 5


@pytest.mark.parametrize("name", ["", "  "])
def test_blank_name_is_rejected(name):
    with pytest.raises(ValueError):
        Member("m1", name)


def test_new_member_can_borrow():
    assert Member("m1", "Ana").can_borrow() is True


def test_add_borrowed_book_records_isbn():
    member = Member("m1", "Ana")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_at_limit_cannot_borrow():
    member = Member("m1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    assert member.can_borrow() is False


def test_add_borrowed_book_beyond_limit_raises_error():
    member = Member("m1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(LibraryError):
        member.add_borrowed_book("0987654321")


def test_borrowing_same_book_twice_raises_error():
    member = Member("m1", "Ana")
    member.add_borrowed_book("1234567890")
    with pytest.raises(LibraryError):
        member.add_borrowed_book("1234567890")


def test_return_book_removes_isbn():
    member = Member("m1", "Ana")
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.borrowed_books == []


def test_returning_unborrowed_book_raises_error():
    member = Member("m1", "Ana")
    with pytest.raises(LibraryError):
        member.return_book("1234567890")


@pytest.mark.parametrize("category,limit", [
    (MemberCategory.STUDENT, 3),
    (MemberCategory.FACULTY, 5),
    (MemberCategory.PUBLIC, 2),
])
def test_category_sets_the_borrow_limit(category, limit):
    assert Member("m1", "Ana", category=category).max_borrow_limit == limit


def test_member_is_a_student_by_default():
    assert Member("m1", "Ana").category is MemberCategory.STUDENT


def test_explicit_limit_overrides_the_category_limit():
    member = Member("m1", "Ana", max_borrow_limit=1, category=MemberCategory.FACULTY)
    assert member.max_borrow_limit == 1


@pytest.mark.parametrize("category,rate", [
    (MemberCategory.STUDENT, 1.0),
    (MemberCategory.FACULTY, 0.5),
    (MemberCategory.PUBLIC, 1.5),
])
def test_category_has_a_daily_late_fee_rate(category, rate):
    assert category.late_fee_rate == rate
