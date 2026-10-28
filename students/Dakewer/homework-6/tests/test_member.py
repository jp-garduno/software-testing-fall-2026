import pytest

from src.member import Member


def test_member_can_be_created():
    member = Member("M001", "Alice")
    assert member.name == "Alice"


def test_member_has_default_borrow_limit_of_three():
    member = Member("M001", "Alice")
    assert member.max_borrow_limit == 3


def test_member_starts_with_no_borrowed_books():
    member = Member("M001", "Alice")
    assert member.borrowed_books == []


def test_member_can_borrow_when_below_limit():
    member = Member("M001", "Alice")
    assert member.can_borrow() is True


def test_add_borrowed_book_records_isbn():
    member = Member("M001", "Alice")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_cannot_borrow_at_limit():
    member = Member("M001", "Alice", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    assert member.can_borrow() is False


def test_add_borrowed_book_fails_beyond_limit():
    member = Member("M001", "Alice", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError):
        member.add_borrowed_book("0987654321")


def test_return_book_removes_isbn_from_borrowed_books():
    member = Member("M001", "Alice")
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.borrowed_books == []


def test_return_book_fails_with_clear_message_when_not_borrowed():
    member = Member("M001", "Alice")
    with pytest.raises(ValueError, match="not borrowed"):
        member.return_book("1234567890")


def test_member_cannot_borrow_same_book_twice():
    member = Member("M001", "Alice")
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="already borrowed"):
        member.add_borrowed_book("1234567890")


def test_member_requires_id():
    with pytest.raises(ValueError, match="id is required"):
        Member("", "Alice")


def test_member_requires_name():
    with pytest.raises(ValueError, match="name is required"):
        Member("M001", "  ")
