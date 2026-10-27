import pytest

from member import Member, MemberCategory

ISBNS = ["0306406152", "0131103628", "0201633612"]


@pytest.fixture(name="member")
def fixture_member():
    return Member("M001", "Ada Lovelace")


def test_member_is_created_with_id_name_and_no_books(member):
    assert (member.member_id, member.name, member.borrowed_books) == ("M001", "Ada Lovelace", [])


def test_member_borrow_limit_defaults_to_three(member):
    assert member.max_borrow_limit == 3


def test_new_member_can_borrow(member):
    assert member.can_borrow() is True


def test_add_borrowed_book_records_the_isbn(member):
    member.add_borrowed_book(ISBNS[0])

    assert member.borrowed_books == [ISBNS[0]]


def test_member_at_the_limit_cannot_borrow(member):
    for isbn in ISBNS:
        member.add_borrowed_book(isbn)

    assert member.can_borrow() is False


def test_add_borrowed_book_beyond_the_limit_is_rejected(member):
    for isbn in ISBNS:
        member.add_borrowed_book(isbn)

    with pytest.raises(ValueError, match="borrow limit of 3"):
        member.add_borrowed_book("0596007124")


def test_add_the_same_book_twice_is_rejected(member):
    member.add_borrowed_book(ISBNS[0])

    with pytest.raises(ValueError, match="already borrowed"):
        member.add_borrowed_book(ISBNS[0])


def test_return_book_removes_the_isbn(member):
    member.add_borrowed_book(ISBNS[0])

    member.return_book(ISBNS[0])

    assert member.borrowed_books == []


def test_return_a_book_that_was_not_borrowed_is_rejected(member):
    with pytest.raises(ValueError, match="has not borrowed"):
        member.return_book(ISBNS[0])


def test_member_category_defaults_to_student(member):
    assert member.category is MemberCategory.STUDENT


def test_faculty_member_can_borrow_five_books():
    assert Member("F001", "Donald Knuth", MemberCategory.FACULTY).max_borrow_limit == 5


def test_public_member_can_borrow_two_books():
    assert Member("P001", "Alan Turing", MemberCategory.PUBLIC).max_borrow_limit == 2
