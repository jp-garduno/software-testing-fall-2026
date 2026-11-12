import pytest
from member import Member

def test_member_creation():
    member = Member(1, "Alice", "Student")
    assert member.max_borrow_limit == 3

def test_invalid_category():
    with pytest.raises(ValueError, match="Invalid category"):
        Member(1, "Alice", "Alien")

def test_can_borrow():
    member = Member(1, "Alice", "Public")
    assert member.can_borrow()

def test_add_borrowed_book():
    member = Member(1, "Alice", "Public")
    member.add_borrowed_book("1234567890")
    assert "1234567890" in member.borrowed_books

def test_borrow_limit_reached():
    member = Member(1, "Alice", "Public") # Limit 2
    member.add_borrowed_book("1111111111")
    member.add_borrowed_book("2222222222")
    with pytest.raises(ValueError, match="Borrow limit reached"):
        member.add_borrowed_book("3333333333")

def test_return_book():
    member = Member(1, "Alice", "Public")
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert "1234567890" not in member.borrowed_books

def test_late_fee_calculation():
    member = Member(1, "Alice")
    member.calculate_late_fee(16) # 2 days late
    assert member.late_fees == 2.0