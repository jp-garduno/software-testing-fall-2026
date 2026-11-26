import pytest

from book import Book
from library import Library
from member import Member, MemberCategory

ISBN = "1234567890"


@pytest.fixture
def library(clock):
    lib = Library(clock=clock)
    lib.add_book(Book(ISBN, "Book One", "Author", copies=5))
    return lib


@pytest.mark.parametrize(
    "category, limit",
    [(MemberCategory.STUDENT, 3), (MemberCategory.FACULTY, 5), (MemberCategory.PUBLIC, 2)],
)
def test_borrow_limit_depends_on_category(category, limit):
    assert Member("m1", "Alice", category=category).max_borrow_limit == limit


def test_faculty_pay_half_the_student_late_fee(library, clock):
    library.register_member(Member("f1", "Prof", category=MemberCategory.FACULTY))
    library.borrow_book("f1", ISBN)
    clock.advance(18)
    assert library.calculate_late_fee("f1", ISBN) == 2.0


def test_public_members_pay_a_higher_late_fee(library, clock):
    library.register_member(Member("p1", "Guest", category=MemberCategory.PUBLIC))
    library.borrow_book("p1", ISBN)
    clock.advance(16)
    assert library.calculate_late_fee("p1", ISBN) == 3.0


def test_public_members_cannot_borrow_a_third_book(library):
    library.add_book(Book("0987654321", "Book Two", "Author", copies=5))
    library.add_book(Book("1111111111", "Book Three", "Author", copies=5))
    library.register_member(Member("p1", "Guest", category=MemberCategory.PUBLIC))
    library.borrow_book("p1", ISBN)
    library.borrow_book("p1", "0987654321")
    with pytest.raises(ValueError, match="limit"):
        library.borrow_book("p1", "1111111111")


def test_explicit_limit_overrides_the_category_default():
    member = Member("f1", "Prof", max_borrow_limit=1, category=MemberCategory.FACULTY)
    assert member.max_borrow_limit == 1
