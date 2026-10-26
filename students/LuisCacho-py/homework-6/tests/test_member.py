import pytest
from src.member import Member


def test_member_can_be_created_with_default_limit():
    member = Member("M001", "Alice Smith")
    assert member.member_id == "M001"
    assert member.name == "Alice Smith"
    assert member.borrowed_books == []
    assert member.max_borrow_limit == 3


def test_member_can_be_created_with_custom_limit():
    member = Member("M002", "Bob Jones", max_borrow_limit=5)
    assert member.max_borrow_limit == 5


def test_member_rejects_empty_id():
    with pytest.raises(ValueError, match="Member ID is required"):
        Member("", "Alice")


def test_member_rejects_empty_name():
    with pytest.raises(ValueError, match="Member name is required"):
        Member("M001", "  ")


def test_member_rejects_negative_limit():
    with pytest.raises(ValueError, match="Max borrow limit must be positive"):
        Member("M001", "Alice", max_borrow_limit=0)
