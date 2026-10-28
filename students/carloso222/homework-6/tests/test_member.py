from src.member import Member


def test_member_can_be_created_with_id_and_name():
    member = Member("M1", "Ana")
    assert (member.member_id, member.name) == ("M1", "Ana")


def test_new_member_has_no_borrowed_books():
    member = Member("M1", "Ana")
    assert member.borrowed_books == []


def test_member_default_borrow_limit_is_three():
    member = Member("M1", "Ana")
    assert member.max_borrow_limit == 3


def test_member_borrow_limit_can_be_overridden():
    member = Member("M1", "Ana", max_borrow_limit=1)
    assert member.max_borrow_limit == 1


def test_member_can_borrow_when_under_limit():
    member = Member("M1", "Ana")
    assert member.can_borrow() is True
