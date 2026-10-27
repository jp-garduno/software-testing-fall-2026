"""Tests for member categories (advanced feature 5)."""

from decimal import Decimal

from src.member import Member, MemberCategory


def test_faculty_member_can_borrow_five_books():
    member = Member("F001", "Alan Turing", category=MemberCategory.FACULTY)
    assert member.max_borrow_limit == 5


def test_public_member_can_borrow_two_books():
    member = Member("P001", "Joan Clarke", category=MemberCategory.PUBLIC)
    assert member.max_borrow_limit == 2


def test_member_defaults_to_student_category():
    assert Member("S001", "Ada Lovelace").category is MemberCategory.STUDENT


def test_faculty_pays_half_the_standard_daily_late_fee():
    assert MemberCategory.FACULTY.daily_late_fee == Decimal("0.50")
