import pytest

from src.exceptions import BookNotBorrowedError, BorrowLimitReachedError
from src.member import Member


def test_member_can_be_created_with_id_and_name():
    member = Member("M1", "Ana")
    assert (member.member_id, member.name) == ("M1", "Ana")


def test_new_member_has_no_borrowed_books():
    member = Member("M1", "Ana")
    assert member.borrowed_books == []


def test_member_default_borrow_limit_is_three():
    member = Member("M1", "Ana")
    assert member.max_borrow_limit == 3


def test_member_borrow_limit_can_be_overridden():
    member = Member("M1", "Ana", max_borrow_limit=1)
    assert member.max_borrow_limit == 1


def test_member_can_borrow_when_under_limit():
    member = Member("M1", "Ana")
    assert member.can_borrow() is True


def test_add_borrowed_book_records_the_isbn():
    member = Member("M1", "Ana")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_cannot_borrow_when_limit_is_reached():
    member = Member("M1", "Ana", max_borrow_limit=2)
    member.add_borrowed_book("1111111111")
    member.add_borrowed_book("2222222222")
    assert member.can_borrow() is False


def test_add_borrowed_book_raises_beyond_limit():
    member = Member("M1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1111111111")
    with pytest.raises(BorrowLimitReachedError):
        member.add_borrowed_book("2222222222")


def test_return_book_removes_the_isbn():
    member = Member("M1", "Ana")
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.borrowed_books == []


def test_member_can_borrow_again_after_returning():
    member = Member("M1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.can_borrow() is True


def test_return_book_raises_for_book_not_borrowed():
    member = Member("M1", "Ana")
    with pytest.raises(BookNotBorrowedError):
        member.return_book("1234567890")


def test_has_borrowed_is_true_only_for_held_books():
    member = Member("M1", "Ana")
    member.add_borrowed_book("1234567890")
    assert (member.has_borrowed("1234567890"), member.has_borrowed("0000000000")) == (True, False)


def test_member_repr_shows_id_and_name():
    assert repr(Member("M1", "Ana")) == "Member(member_id='M1', name='Ana')"
