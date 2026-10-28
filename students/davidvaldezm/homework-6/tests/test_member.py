import pytest

from src.member import Member


def test_member_has_identity_and_default_limit():
    member = Member("M1", "Ana")
    assert (member.member_id, member.name, member.borrowed_books, member.max_borrow_limit) == ("M1", "Ana", [], 3)
