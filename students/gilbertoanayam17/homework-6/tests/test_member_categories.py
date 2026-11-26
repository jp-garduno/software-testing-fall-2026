"""Tests for member categories: each one has its own borrow limit and late fee rate."""

from datetime import date
from unittest.mock import Mock

import pytest

from src.book import Book
from src.library import Library
from src.member import Member, MemberCategory


def test_should_let_faculty_borrow_up_to_five_books():
    member = Member("F1", "Luis Perez", category=MemberCategory.FACULTY)

    assert member.max_borrow_limit == 5


def test_should_limit_public_members_to_two_books():
    member = Member("P1", "Eva Ruiz", category=MemberCategory.PUBLIC)

    assert member.max_borrow_limit == 2


def test_should_treat_members_as_students_by_default():
    assert Member("S1", "Ana Lopez").category is MemberCategory.STUDENT


@pytest.mark.parametrize(
    "category, expected_fee",
    [(MemberCategory.STUDENT, 4.0), (MemberCategory.FACULTY, 2.0), (MemberCategory.PUBLIC, 6.0)],
    ids=["student", "faculty", "public"],
)
def test_should_charge_each_category_its_own_daily_late_fee(category, expected_fee):
    clock = Mock(return_value=date(2026, 1, 1))
    library = Library(clock=clock)
    library.add_book(Book("1234567890", "Clean Code", "Robert C. Martin"))
    library.register_member(Member("M1", "Ana Lopez", category=category))
    library.borrow_book("M1", "1234567890")

    clock.return_value = date(2026, 1, 19)

    assert library.calculate_late_fees("M1") == expected_fee
