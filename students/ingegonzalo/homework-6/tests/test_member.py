import pytest

from src.member import Member

def test_member_can_be_created():
    member = Member("M001", "Ana")
    assert member.name == "Ana"

def test_member_starts_with_no_borrowed_books():
    member = Member("M001", "Ana")
    assert member.borrowed_books == []

def test_member_has_default_borrow_limit_of_three():
    member = Member("M001", "Ana")
    assert member.max_borrow_limit == 3