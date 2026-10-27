"""Tests for the Member class."""

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
