from datetime import date
import pytest
from src.book import Book
from src.member import Member, MemberCategory
from src.library import Library


def test_member_categories_default_limits_and_rates():
    faculty = Member("M001", "Dr. Turing", category=MemberCategory.FACULTY)
    student = Member("M002", "Ada Lovelace", category=MemberCategory.STUDENT)
    public = Member("M003", "Grace Hopper", category=MemberCategory.PUBLIC)

    assert faculty.max_borrow_limit == 5
    assert faculty.daily_fee_rate == 0.25

    assert student.max_borrow_limit == 3
    assert student.daily_fee_rate == 0.50

    assert public.max_borrow_limit == 2
    assert public.daily_fee_rate == 1.00


def test_member_rejects_invalid_category():
    with pytest.raises(ValueError, match="Invalid member category"):
        Member("M001", "Invalid", category="SUPERUSER")


def test_library_late_fees_apply_member_category_rates():
    lib = Library()
    book1 = Book("1111111111", "Faculty Book", "Author", total_copies=2)
    book2 = Book("2222222222", "Student Book", "Author", total_copies=2)
    book3 = Book("3333333333", "Public Book", "Author", total_copies=2)

    faculty = Member("F001", "Dr. Smith", category=MemberCategory.FACULTY)
    student = Member("S001", "Bob Student", category=MemberCategory.STUDENT)
    public = Member("P001", "Jane Public", category=MemberCategory.PUBLIC)

    lib.add_book(book1)
    lib.add_book(book2)
    lib.add_book(book3)
    lib.register_member(faculty)
    lib.register_member(student)
    lib.register_member(public)

    # All borrow on Oct 1, checked on Oct 25 (10 days overdue)
    borrow_date = date(2026, 10, 1)
    as_of_date = date(2026, 10, 25)

    lib.borrow_book("F001", "1111111111", borrow_date=borrow_date)
    lib.borrow_book("S001", "2222222222", borrow_date=borrow_date)
    lib.borrow_book("P001", "3333333333", borrow_date=borrow_date)

    # Faculty: 10 days * $0.25 = $2.50
    assert lib.calculate_member_late_fees("F001", as_of_date=as_of_date) == 2.50
    # Student: 10 days * $0.50 = $5.00
    assert lib.calculate_member_late_fees("S001", as_of_date=as_of_date) == 5.00
    # Public: 10 days * $1.00 = $10.00
    assert lib.calculate_member_late_fees("P001", as_of_date=as_of_date) == 10.00
