"""Tests for the Member class."""

from src.member import Member


def test_member_is_created_with_id_and_name():
    member = Member("M001", "Ada Lovelace")
    assert (member.member_id, member.name) == ("M001", "Ada Lovelace")
