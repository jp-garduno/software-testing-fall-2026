"""Tests for Member: identity, borrow limit and the books a member holds."""

import pytest

from src import errors
from src.member import Member


def test_should_store_id_and_name_when_created():
    member = Member("M1", "Ana Lopez")

    assert (member.member_id, member.name) == ("M1", "Ana Lopez")


def test_should_start_with_no_borrowed_books():
    assert not Member("M1", "Ana Lopez").borrowed_books


def test_should_have_default_borrow_limit_of_three():
    assert Member("M1", "Ana Lopez").max_borrow_limit == 3


def test_should_record_book_when_added_to_borrowed_books():
    member = Member("M1", "Ana Lopez")

    member.add_borrowed_book("1234567890")

    assert member.borrowed_books == ["1234567890"]


def test_should_not_be_able_to_borrow_when_limit_reached():
    member = Member("M1", "Ana Lopez", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")

    assert not member.can_borrow()


def test_should_raise_error_when_adding_book_beyond_limit():
    member = Member("M1", "Ana Lopez", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")

    with pytest.raises(errors.BorrowLimitExceededError):
        member.add_borrowed_book("9780132350884")


def test_should_remove_book_when_returned():
    member = Member("M1", "Ana Lopez")
    member.add_borrowed_book("1234567890")

    member.return_book("1234567890")

    assert not member.borrowed_books


def test_should_raise_error_when_returning_book_not_borrowed():
    member = Member("M1", "Ana Lopez")

    with pytest.raises(errors.InvalidReturnError):
        member.return_book("1234567890")
