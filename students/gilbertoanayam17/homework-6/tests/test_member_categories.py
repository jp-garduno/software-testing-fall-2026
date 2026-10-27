"""Tests for member categories: each one has its own borrow limit and late fee rate."""

from src.member import Member, MemberCategory


def test_should_let_faculty_borrow_up_to_five_books():
    member = Member("F1", "Luis Perez", category=MemberCategory.FACULTY)

    assert member.max_borrow_limit == 5
