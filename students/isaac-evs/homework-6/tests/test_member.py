from member import Member


def test_member_has_a_name():
    member = Member("m1", "Alice")
    assert member.name == "Alice"


def test_member_starts_with_no_borrowed_books():
    assert Member("m1", "Alice").borrowed_books == []
