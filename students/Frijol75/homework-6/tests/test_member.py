import pytest
from src.member import Member


def test_member_creation_with_default_limit():
    member = Member(member_id="M001", name="Alice Johnson")
    assert member.member_id == "M001"
    assert member.name == "Alice Johnson"
    assert member.borrowed_books == []
    assert member.max_borrow_limit == 3


def test_member_creation_with_custom_limit():
    member = Member(member_id="M002", name="Bob Smith", max_borrow_limit=5)
    assert member.max_borrow_limit == 5


def test_member_creation_rejects_empty_id():
    with pytest.raises(ValueError, match="Member ID is required"):
        Member(member_id="", name="Valid Name")


def test_member_creation_rejects_empty_name():
    with pytest.raises(ValueError, match="Member name is required"):
        Member(member_id="M001", name="   ")


def test_member_creation_rejects_non_positive_limit():
    with pytest.raises(ValueError, match="Max borrow limit must be positive"):
        Member(member_id="M001", name="Valid Name", max_borrow_limit=0)


def test_member_can_borrow_when_under_limit():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=2)
    assert member.can_borrow() is True


def test_member_cannot_borrow_when_at_limit():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=2)
    member.borrowed_books = ["1234567890", "0987654321"]
    assert member.can_borrow() is False
