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

def test_return_book_removes_isbn_from_borrowed_books():
    member = Member("M001", "Ana")
    member.add_borrowed_book("1111111111")
    member.return_book("1111111111")
    assert "1111111111" not in member.borrowed_books

def test_return_book_raises_error_when_not_borrowed():
    member = Member("M001", "Ana")
    with pytest.raises(ValueError, match="not borrowed"):
        member.return_book("1111111111")

def test_member_requires_name():
    with pytest.raises(ValueError):
        Member("M001", "")

def test_member_starts_with_no_late_fees():
    member = Member("M001", "Ana")
    assert member.late_fees == 0

def test_add_late_fee_accumulates_total():
    member = Member("M001", "Ana")
    member.add_late_fee(3)
    member.add_late_fee(2)
    assert member.late_fees == 5

def test_member_category_defaults_to_student():
    member = Member("M001", "Ana")
    assert member.category == "student"

def test_faculty_member_has_borrow_limit_of_five():
    member = Member("M002", "Dr. Ruiz", category="faculty")
    assert member.max_borrow_limit == 5

def test_public_member_has_borrow_limit_of_two():
    member = Member("M003", "Visitante", category="public")
    assert member.max_borrow_limit == 2

def test_member_rejects_unknown_category():
    with pytest.raises(ValueError, match="category"):
        Member("M001", "Ana", category="alien")

@pytest.mark.parametrize("category, rate", [
    ("student", 1),
    ("faculty", 0.5),
    ("public", 2),
])
def test_member_late_fee_rate_depends_on_category(category, rate):
    member = Member("M001", "Ana", category=category)
    assert member.late_fee_rate == rate