"""Behavioral tests for library members."""

import pytest

from src.member import Member


def test_member_stores_identity_and_default_borrow_limit():
    member = Member("m1", "Luis")
    assert (member.member_id, member.name, member.borrowed_books,
            member.max_borrow_limit) == ("m1", "Luis", [], 3)


def test_new_member_can_borrow():
    assert Member("m1", "Luis").can_borrow() is True
