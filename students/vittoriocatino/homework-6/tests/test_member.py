from member import Member


def test_member_is_created_with_default_limit():
    member = Member("m-1", "Ada Lovelace")

    assert member.max_borrow_limit == 3
