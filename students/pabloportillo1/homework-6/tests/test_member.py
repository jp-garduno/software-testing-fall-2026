from member import Member


def test_member_is_created_with_id_name_and_no_books():
    member = Member("M001", "Ada Lovelace")

    assert (member.member_id, member.name, member.borrowed_books) == ("M001", "Ada Lovelace", [])


def test_member_borrow_limit_defaults_to_three():
    assert Member("M001", "Ada Lovelace").max_borrow_limit == 3
