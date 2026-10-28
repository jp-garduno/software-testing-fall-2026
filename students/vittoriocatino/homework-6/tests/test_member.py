from member import Member
import pytest


def test_member_is_created_with_default_limit():
    member = Member("m-1", "Ada Lovelace")

    assert member.max_borrow_limit == 3


def test_member_can_borrow_until_limit():
    member = Member("m-1", "Ada", max_borrow_limit=1)

    assert member.can_borrow() is True
    member.add_borrowed_book("1234567890")
    assert member.can_borrow() is False


def test_member_can_return_a_borrowed_book():
    member = Member("m-1", "Ada")
    member.add_borrowed_book("1234567890")

    member.return_book("1234567890")

    assert member.borrowed_books == []


@pytest.mark.parametrize(
    ("category", "limit", "fee_rate"),
    [("student", 3, 1.0), ("faculty", 5, 0.5), ("public", 2, 1.5)],
)
def test_member_category_configures_limits_and_fee_rates(category, limit, fee_rate):
    member = Member("m-1", "Ada", category=category)

    assert (member.max_borrow_limit, member.late_fee_rate) == (limit, fee_rate)
