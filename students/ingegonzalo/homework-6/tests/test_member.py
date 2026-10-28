import pytest

from src.member import Member

def test_member_can_be_created():
    member = Member("M001", "Ana")
    assert member.name == "Ana"

def test_member_starts_with_no_borrowed_books():
    member = Member("M001", "Ana")
    assert member.borrowed_books == []

def test_member_has_default_borrow_limit_of_three():
    member = Member("M001", "Ana")
    assert member.max_borrow_limit == 3

def test_member_can_have_custom_borrow_limit():
    member = Member("M001", "Ana", max_borrow_limit=5)
    assert member.max_borrow_limit == 5

def test_add_borrowed_book_adds_isbn_to_list():
    member = Member("M001", "Ana")
    member.add_borrowed_book("1234567890")
    assert "1234567890" in member.borrowed_books

def test_member_can_borrow_when_under_limit():
    member = Member("M001", "Ana")
    assert member.can_borrow() is True

def test_member_cannot_borrow_when_limit_reached():
    member = Member("M001", "Ana")
    member.add_borrowed_book("1111111111")
    member.add_borrowed_book("2222222222")
    member.add_borrowed_book("3333333333")
    assert member.can_borrow() is False

def test_add_borrowed_book_raises_error_when_limit_reached():
    member = Member("M001", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1111111111")
    with pytest.raises(ValueError):
        member.add_borrowed_book("2222222222")

def test_add_borrowed_book_rejects_duplicate_isbn():
    member = Member("M001", "Ana")
    member.add_borrowed_book("1111111111")
    with pytest.raises(ValueError):
        member.add_borrowed_book("1111111111")