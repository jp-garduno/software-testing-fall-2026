import pytest
from src.member import Member

def test_member_can_be_created():
    m = Member("m1", "Ana")
    assert (m.member_id, m.name) == ("m1", "Ana")

def test_new_member_has_no_borrowed_books():
    assert Member("m1", "Ana").borrowed_books == []

def test_default_borrow_limit_is_three():
    assert Member("m1", "Ana").max_borrow_limit == 3

def test_add_borrowed_book_stores_isbn():
    m = Member("m1", "Ana")
    m.add_borrowed_book("1234567890")
    assert m.borrowed_books == ["1234567890"]

def test_can_borrow_when_under_limit():
    assert Member("m1", "Ana").can_borrow() is True

def test_cannot_borrow_when_limit_reached():
    m = Member("m1", "Ana", max_borrow_limit=1)
    m.add_borrowed_book("1234567890")
    assert m.can_borrow() is False


def test_add_borrowed_book_raises_over_limit():
    m = Member("m1", "Ana", max_borrow_limit=1)
    m.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="limit"):
        m.add_borrowed_book("1234567891")

def test_return_book_removes_isbn():
    m = Member("m1", "Ana")
    m.add_borrowed_book("1234567890")
    m.return_book("1234567890")
    assert m.borrowed_books == []


def test_return_book_not_borrowed_raises():
    with pytest.raises(ValueError, match="not borrowed"):
        Member("m1", "Ana").return_book("1234567890")

def test_faculty_has_limit_of_five():
    assert Member("f1", "Prof", category="faculty").max_borrow_limit == 5
