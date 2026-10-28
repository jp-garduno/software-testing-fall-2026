from member import Member


def test_member_has_a_name():
    member = Member("m1", "Alice")
    assert member.name == "Alice"
