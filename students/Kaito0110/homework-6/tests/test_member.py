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


