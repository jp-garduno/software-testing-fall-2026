"""Behavioral tests for library members."""

import pytest

from src.member import Member


def test_member_stores_identity_and_default_borrow_limit():
    member = Member("m1", "Luis")
    assert (member.member_id, member.name, member.borrowed_books,
            member.max_borrow_limit) == ("m1", "Luis", [], 3)


def test_new_member_can_borrow():
    assert Member("m1", "Luis").can_borrow() is True


def test_add_borrowed_book_records_the_isbn():
    member = Member("m1", "Luis")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_cannot_exceed_a_custom_borrow_limit():
    member = Member("m1", "Luis", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="limit"):
        member.add_borrowed_book("1234567891")


def test_member_cannot_borrow_the_same_isbn_twice():
    member = Member("m1", "Luis")
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="already"):
        member.add_borrowed_book("1234567890")
