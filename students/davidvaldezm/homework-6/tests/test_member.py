import pytest

from src.member import Member


def test_member_has_identity_and_default_limit():
    member = Member("M1", "Ana")
    assert (member.member_id, member.name, member.borrowed_books, member.max_borrow_limit) == ("M1", "Ana", [], 3)


@pytest.mark.parametrize("member_id, name", [("", "Ana"), ("  ", "Ana"), (None, "Ana"), ("M1", ""), ("M1", None)])
def test_member_requires_nonblank_identity(member_id, name):
    with pytest.raises(ValueError, match="required"):
        Member(member_id, name)


@pytest.mark.parametrize("limit", [0, -1, 1.5, True])
def test_member_requires_positive_integer_limit(limit):
    with pytest.raises(ValueError, match="limit"):
        Member("M1", "Ana", max_borrow_limit=limit)
