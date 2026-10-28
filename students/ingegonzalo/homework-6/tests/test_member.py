import pytest

from src.member import Member

def test_member_can_be_created():
    member = Member("M001", "Ana")
    assert member.name == "Ana"