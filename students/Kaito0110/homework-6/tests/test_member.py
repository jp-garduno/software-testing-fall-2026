"""Unit tests for the Member class developed with TDD."""

import pytest
from src.member import Member


def test_member_can_borrow_when_below_limit():
    member = Member(
        member_id="M001",
        name="Ana",
    )

    assert member.can_borrow() is True


def test_member_cannot_borrow_when_limit_is_reached():
    member = Member(
        member_id="M001",
        name="Ana",
        max_borrow_limit=2,
    )

    member.borrowed_books = ["ISBN001", "ISBN002"]

    assert member.can_borrow() is False


def test_member_adds_borrowed_book():
    member = Member(
        member_id="M001",
        name="Ana",
    )

    member.add_borrowed_book("ISBN001")

    assert member.borrowed_books == ["ISBN001"]


def test_member_returns_borrowed_book():
    member = Member(
        member_id="M001",
        name="Ana",
    )
    member.add_borrowed_book("ISBN001")

    member.return_book("ISBN001")

    assert not member.borrowed_books


def test_member_cannot_add_book_when_limit_is_reached():
    member = Member(
        member_id="M001",
        name="Ana",
        max_borrow_limit=1,
    )
    member.add_borrowed_book("ISBN001")

    with pytest.raises(ValueError, match="borrowing limit"):
        member.add_borrowed_book("ISBN002")

    assert member.borrowed_books == ["ISBN001"]


def test_member_cannot_return_book_not_borrowed():
    member = Member(member_id="M001", name="Ana")

    with pytest.raises(ValueError, match="has not borrowed"):
        member.return_book("ISBN999")


def test_member_rejects_negative_borrow_limit():
    with pytest.raises(ValueError, match="borrowing limit"):
        Member(
            member_id="M001",
            name="Ana",
            max_borrow_limit=-1,
        )


def test_member_with_zero_borrow_limit_cannot_borrow():
    member = Member(
        member_id="M001",
        name="Ana",
        max_borrow_limit=0,
    )

    assert member.can_borrow() is False

    with pytest.raises(ValueError, match="borrowing limit"):
        member.add_borrowed_book("ISBN001")

    assert not member.borrowed_books


def test_member_rejects_empty_name():
    with pytest.raises(ValueError, match="name"):
        Member(member_id="M001", name="")


def test_member_rejects_name_with_only_spaces():
    with pytest.raises(ValueError, match="name"):
        Member(member_id="M001", name="   ")


def test_member_rejects_empty_member_id():
    with pytest.raises(ValueError, match="Member ID"):
        Member(member_id="", name="Ana")


def test_member_can_borrow_again_after_returning_book():
    member = Member(
        member_id="M001",
        name="Ana",
        max_borrow_limit=1,
    )

    member.add_borrowed_book("ISBN001")
    member.return_book("ISBN001")

    assert member.can_borrow() is True

    member.add_borrowed_book("ISBN002")

    assert member.borrowed_books == ["ISBN002"]


def test_member_returning_book_keeps_other_borrowed_books():
    member = Member(member_id="M001", name="Ana")

    member.add_borrowed_book("ISBN001")
    member.add_borrowed_book("ISBN002")

    member.return_book("ISBN001")

    assert member.borrowed_books == ["ISBN002"]


def test_member_borrowed_books_count_after_multiple_returns():
    member = Member(member_id="M001", name="Ana")

    member.add_borrowed_book("ISBN001")
    member.add_borrowed_book("ISBN002")
    member.add_borrowed_book("ISBN003")

    member.return_book("ISBN001")
    member.return_book("ISBN003")

    assert member.borrowed_books == ["ISBN002"]
    assert len(member.borrowed_books) == 1
    assert member.can_borrow() is True


def test_member_categories_set_limits_and_late_fee_rates():
    student = Member(member_id="M010", name="Student User", category="student")
    faculty = Member(member_id="M011", name="Faculty User", category="Faculty")
    public = Member(member_id="M012", name="Public User", category="public")

    assert student.max_borrow_limit == 3
    assert student.late_fee_rate == 1.0
    assert faculty.max_borrow_limit == 5
    assert faculty.late_fee_rate == 0.5
    assert public.max_borrow_limit == 2
    assert public.late_fee_rate == 2.0


def test_member_rejects_invalid_category():
    with pytest.raises(ValueError, match="Invalid member category"):
        Member(member_id="M013", name="Invalid User", category="vip")
