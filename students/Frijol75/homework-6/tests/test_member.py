import pytest
from src.member import Member


def test_member_creation_with_default_limit():
    member = Member(member_id="M001", name="Alice Johnson")
    assert member.member_id == "M001"
    assert member.name == "Alice Johnson"
    assert member.borrowed_books == []
    assert member.max_borrow_limit == 3


def test_member_creation_with_custom_limit():
    member = Member(member_id="M002", name="Bob Smith", max_borrow_limit=5)
    assert member.max_borrow_limit == 5


def test_member_creation_rejects_empty_id():
    with pytest.raises(ValueError, match="Member ID is required"):
        Member(member_id="", name="Valid Name")


def test_member_creation_rejects_empty_name():
    with pytest.raises(ValueError, match="Member name is required"):
        Member(member_id="M001", name="   ")


def test_member_creation_rejects_non_positive_limit():
    with pytest.raises(ValueError, match="Max borrow limit must be positive"):
        Member(member_id="M001", name="Valid Name", max_borrow_limit=0)


def test_member_can_borrow_when_under_limit():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=2)
    assert member.can_borrow() is True


def test_member_cannot_borrow_when_at_limit():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=2)
    member.borrowed_books = ["1234567890", "0987654321"]
    assert member.can_borrow() is False


def test_member_add_borrowed_book_success():
    member = Member(member_id="M001", name="Alice")
    member.add_borrowed_book("1234567890")
    assert member.borrowed_books == ["1234567890"]


def test_member_add_borrowed_book_rejects_invalid_identifier():
    member = Member(member_id="M001", name="Alice")
    with pytest.raises(ValueError, match="Invalid book identifier"):
        member.add_borrowed_book("")


def test_member_add_borrowed_book_rejects_when_limit_exceeded():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="Borrow limit reached"):
        member.add_borrowed_book("0987654321")


def test_member_add_borrowed_book_rejects_duplicate_borrow():
    member = Member(member_id="M001", name="Alice", max_borrow_limit=3)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="Book already borrowed by this member"):
        member.add_borrowed_book("1234567890")


def test_member_return_book_success():
    member = Member(member_id="M001", name="Alice")
    member.add_borrowed_book("1234567890")
    member.return_book("1234567890")
    assert member.borrowed_books == []


def test_member_return_book_raises_when_not_borrowed():
    member = Member(member_id="M001", name="Alice")
    with pytest.raises(ValueError, match="Book not borrowed by this member"):
        member.return_book("9999999999")


def test_member_representation_and_equality():
    member1 = Member(member_id="M001", name="Alice")
    member2 = Member(member_id="M001", name="Alice")
    assert repr(member1) == "<Member ID=M001 Name='Alice' Borrowed=0/3>"
    assert member1 == member2
    assert member1 != "other"


def test_member_hash_and_set_operations():
    member1 = Member(member_id="M001", name="Alice")
    member2 = Member(member_id="M001", name="Alice")
    member3 = Member(member_id="M002", name="Bob")
    member_set = {member1, member2, member3}
    assert len(member_set) == 2
    assert hash(member1) == hash("M001")
