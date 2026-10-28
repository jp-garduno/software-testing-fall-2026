from member import Member


def test_member_has_a_name():
    member = Member("m1", "Alice")
    assert member.name == "Alice"


def test_member_starts_with_no_borrowed_books():
    assert Member("m1", "Alice").borrowed_books == []


def test_member_default_borrow_limit_is_three():
    assert Member("m1", "Alice").max_borrow_limit == 3


def test_add_borrowed_book_records_the_isbn():
    member = Member("m1", "Alice")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]
