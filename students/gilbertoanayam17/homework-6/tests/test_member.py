"""Tests for Member: identity, borrow limit and the books a member holds."""

from src.member import Member


def test_should_store_id_and_name_when_created():
    member = Member("M1", "Ana Lopez")

    assert (member.member_id, member.name) == ("M1", "Ana Lopez")
