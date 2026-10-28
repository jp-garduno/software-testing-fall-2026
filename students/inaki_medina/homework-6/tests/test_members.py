import library_system
import pytest

Member = library_system.Member

# Test 1: Member exists
def test_member_can_be_created():
    member = Member("Juan")
    assert member.name == "Juan"
    assert member.member_id is not None
    assert member.borrowed_books == []
    assert member.max_borrow_limit == 3


def test_member_can_borrow_until_limit():
    member = Member("Juan", max_borrow_limit=2)

    assert member.can_borrow()
    member.add_borrowed_book("Book 1")
    assert member.can_borrow()
    member.add_borrowed_book("Book 2")
    assert not member.can_borrow()


def test_member_cannot_borrow_more_than_limit():
    member = Member("Juan", max_borrow_limit=1)
    member.add_borrowed_book("Book 1")

    with pytest.raises(ValueError):
        member.add_borrowed_book("Book 2")


def test_member_can_return_borrowed_book():
    member = Member("Juan")
    member.add_borrowed_book("Book 1")

    member.return_book("Book 1")

    assert member.borrowed_books == []