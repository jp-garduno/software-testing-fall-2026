from decimal import Decimal

import pytest

from exceptions import BorrowLimitExceededError, InvalidReturnError
from member import Member, MemberCategory

CLEAN_CODE = "0306406152"
CLEAN_CODER = "9780132350884"


def test_member_is_created_without_borrowed_books():
    member = Member("M001", "Ana Lopez")
    assert (member.member_id, member.name, member.borrowed_books) == (
        "M001",
        "Ana Lopez",
        [],
    )


def test_member_has_default_borrow_limit_of_three():
    assert Member("M001", "Ana Lopez").max_borrow_limit == 3


def test_member_can_borrow_when_under_limit():
    assert Member("M001", "Ana Lopez").can_borrow() is True


def test_add_borrowed_book_records_isbn():
    member = Member("M001", "Ana Lopez")
    member.add_borrowed_book(CLEAN_CODE)
    assert member.borrowed_books == [CLEAN_CODE]


def test_add_borrowed_book_raises_when_limit_reached():
    member = Member("M001", "Ana Lopez", max_borrow_limit=1)
    member.add_borrowed_book(CLEAN_CODE)
    with pytest.raises(BorrowLimitExceededError):
        member.add_borrowed_book(CLEAN_CODER)


def test_return_book_removes_isbn():
    member = Member("M001", "Ana Lopez")
    member.add_borrowed_book(CLEAN_CODE)
    member.return_book(CLEAN_CODE)
    assert member.borrowed_books == []


def test_return_book_raises_when_book_was_not_borrowed():
    with pytest.raises(InvalidReturnError):
        Member("M001", "Ana Lopez").return_book(CLEAN_CODE)


@pytest.mark.parametrize(
    ("category", "limit"),
    [
        (MemberCategory.STUDENT, 3),
        (MemberCategory.FACULTY, 5),
        (MemberCategory.PUBLIC, 2),
    ],
)
def test_borrow_limit_depends_on_member_category(category, limit):
    assert Member("M002", "Dra. Ruiz", category=category).max_borrow_limit == limit


@pytest.mark.parametrize(
    ("category", "fee"),
    [
        (MemberCategory.STUDENT, Decimal("1.00")),
        (MemberCategory.FACULTY, Decimal("0.50")),
        (MemberCategory.PUBLIC, Decimal("1.50")),
    ],
)
def test_daily_late_fee_depends_on_member_category(category, fee):
    assert Member("M002", "Dra. Ruiz", category=category).daily_late_fee == fee
