"""Tests for member categories: each one has its own borrow limit and late fee rate."""

from src.member import Member, MemberCategory


def test_should_let_faculty_borrow_up_to_five_books():
    member = Member("F1", "Luis Perez", category=MemberCategory.FACULTY)

    assert member.max_borrow_limit == 5


def test_should_limit_public_members_to_two_books():
    member = Member("P1", "Eva Ruiz", category=MemberCategory.PUBLIC)

    assert member.max_borrow_limit == 2


def test_should_treat_members_as_students_by_default():
    assert Member("S1", "Ana Lopez").category is MemberCategory.STUDENT
