import pytest

from member import Member


def test_member_has_a_name():
    member = Member("m1", "Alice")
    assert member.name == "Alice"


def test_member_starts_with_no_borrowed_books():
    assert Member("m1", "Alice").borrowed_books == []


def test_member_default_borrow_limit_is_three():
    assert Member("m1", "Alice").max_borrow_limit == 3


def test_add_borrowed_book_records_the_isbn():
    member = Member("m1", "Alice")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_can_borrow_when_under_limit():
    assert Member("m1", "Alice").can_borrow() is True


def test_member_cannot_borrow_at_the_limit():
    member = Member("m1", "Alice", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    assert member.can_borrow() is False


def test_add_borrowed_book_fails_beyond_the_limit():
    member = Member("m1", "Alice", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="limit"):
        member.add_borrowed_book("0987654321")


def test_return_book_removes_the_isbn():
    member = Member("m1", "Alice")
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.borrowed_books == []


def test_return_book_fails_when_not_borrowed():
    with pytest.raises(ValueError, match="not borrowed"):
        Member("m1", "Alice").return_book("1234567890")
