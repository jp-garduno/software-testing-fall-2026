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


def test_member_can_borrow_when_under_limit():
    member = Member("M001", "Alice Smith", max_borrow_limit=2)
    assert member.can_borrow() is True


def test_member_cannot_borrow_when_at_limit():
    member = Member("M001", "Alice Smith", max_borrow_limit=2)
    member.borrowed_books = ["1111111111", "2222222222"]
    assert member.can_borrow() is False


def test_member_add_borrowed_book_success():
    member = Member("M001", "Alice Smith", max_borrow_limit=2)
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_add_borrowed_book_exceeds_limit():
    member = Member("M001", "Alice Smith", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="Borrow limit reached"):
        member.add_borrowed_book("0987654321")


def test_member_return_book_success():
    member = Member("M001", "Alice Smith", max_borrow_limit=2)
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.borrowed_books == []


def test_member_return_book_not_borrowed():
    member = Member("M001", "Alice Smith", max_borrow_limit=2)
    with pytest.raises(ValueError, match="Book was not borrowed by this member"):
        member.return_book("1234567890")
