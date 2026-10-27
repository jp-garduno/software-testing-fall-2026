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
