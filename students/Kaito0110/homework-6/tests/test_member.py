"""Unit tests for the Member class developed with TDD."""

import pytest
from src.member import Member


def test_member_can_borrow_when_below_limit():
    member = Member(
        member_id="M001",
        name="Ana",
    )

    assert member.can_borrow() is True


def test_member_cannot_borrow_when_limit_is_reached():
    member = Member(
        member_id="M001",
        name="Ana",
        max_borrow_limit=2,
    )

    member.borrowed_books = ["ISBN001", "ISBN002"]

    assert member.can_borrow() is False


def test_member_adds_borrowed_book():
    member = Member(
        member_id="M001",
        name="Ana",
    )

    member.add_borrowed_book("ISBN001")

    assert member.borrowed_books == ["ISBN001"]


def test_member_returns_borrowed_book():
    member = Member(
        member_id="M001",
        name="Ana",
    )
    member.add_borrowed_book("ISBN001")

    member.return_book("ISBN001")

    assert not member.borrowed_books


def test_member_cannot_add_book_when_limit_is_reached():
    member = Member(
        member_id="M001",
        name="Ana",
        max_borrow_limit=1,
    )
    member.add_borrowed_book("ISBN001")

    with pytest.raises(ValueError, match="borrowing limit"):
        member.add_borrowed_book("ISBN002")

    assert member.borrowed_books == ["ISBN001"]


def test_member_cannot_return_book_not_borrowed():
    member = Member(member_id="M001", name="Ana")

    with pytest.raises(ValueError, match="has not borrowed"):
        member.return_book("ISBN999")


