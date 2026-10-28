import pytest

from src.member import Member

def test_member_can_be_created():
    member = Member("M001", "Ana")
    assert member.name == "Ana"

def test_member_starts_with_no_borrowed_books():
    member = Member("M001", "Ana")
    assert member.borrowed_books == []