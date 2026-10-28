import pytest

from src.member import Member


def test_member_has_identity_and_default_limit():
    member = Member("M1", "Ana")
    assert (member.member_id, member.name, member.borrowed_books, member.max_borrow_limit) == ("M1", "Ana", [], 3)


@pytest.mark.parametrize("member_id, name", [("", "Ana"), ("  ", "Ana"), (None, "Ana"), ("M1", ""), ("M1", None)])
def test_member_requires_nonblank_identity(member_id, name):
    with pytest.raises(ValueError, match="required"):
        Member(member_id, name)


@pytest.mark.parametrize("limit", [0, -1, 1.5, True])
def test_member_requires_positive_integer_limit(limit):
    with pytest.raises(ValueError, match="limit"):
        Member("M1", "Ana", max_borrow_limit=limit)


def test_new_member_can_borrow():
    assert Member("M1", "Ana").can_borrow() is True


def test_member_records_a_borrowed_isbn():
    member = Member("M1", "Ana")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_cannot_exceed_custom_limit():
    member = Member("M1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="limit"):
        member.add_borrowed_book("1234567890123")
    assert member.can_borrow() is False


def test_member_cannot_borrow_same_isbn_twice():
    member = Member("M1", "Ana")
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="already"):
        member.add_borrowed_book("1234567890")


def test_member_return_frees_capacity():
    member = Member("M1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.can_borrow() is True


def test_member_rejects_return_without_a_loan():
    with pytest.raises(ValueError, match="not borrowed"):
        Member("M1", "Ana").return_book("1234567890")
