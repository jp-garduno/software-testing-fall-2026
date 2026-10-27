"""Tests for the Member class."""

import pytest

from src.exceptions import BorrowLimitExceededError
from src.member import Member


def test_member_is_created_with_id_and_name():
    member = Member("M001", "Ada Lovelace")
    assert (member.member_id, member.name) == ("M001", "Ada Lovelace")


def test_new_member_has_no_borrowed_books():
    assert Member("M001", "Ada Lovelace").borrowed_books == []


def test_default_borrow_limit_is_three():
    assert Member("M001", "Ada Lovelace").max_borrow_limit == 3


def test_add_borrowed_book_records_the_isbn():
    member = Member("M001", "Ada Lovelace")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_can_borrow_when_under_limit():
    assert Member("M001", "Ada Lovelace").can_borrow() is True


def test_member_cannot_borrow_when_limit_reached():
    member = Member("M001", "Ada Lovelace", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    assert member.can_borrow() is False


def test_add_borrowed_book_beyond_limit_raises():
    member = Member("M001", "Ada Lovelace", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(BorrowLimitExceededError):
        member.add_borrowed_book("0987654321")


def test_return_book_removes_it_from_borrowed_books():
    member = Member("M001", "Ada Lovelace")
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.borrowed_books == []


def test_return_book_not_borrowed_raises():
    member = Member("M001", "Ada Lovelace")
    with pytest.raises(ValueError, match="has not borrowed"):
        member.return_book("1234567890")


@pytest.mark.parametrize("name", ["", "  ", None])
def test_member_without_name_is_rejected(name):
    with pytest.raises(ValueError):
        Member("M001", name)
