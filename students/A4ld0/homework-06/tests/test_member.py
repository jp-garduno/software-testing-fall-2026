import pytest
from src.member import Member


def test_member_defaults_and_independent_lists():
    first, second = Member("m1", "Ana"), Member("m2", "Luis")
    first.borrowed_books.append("1234567890")
    assert (first.member_id, first.name, first.max_borrow_limit, second.borrowed_books) == ("m1", "Ana", 3, [])


def test_custom_borrow_limit():
    assert Member("m1", "Ana", max_borrow_limit=5).max_borrow_limit == 5


@pytest.mark.parametrize("limit, expected", [(0, False), (3, True)])
def test_member_can_borrow(limit, expected):
    assert Member("m1", "Ana", limit).can_borrow() is expected
