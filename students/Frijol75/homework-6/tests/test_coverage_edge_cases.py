from datetime import date
import pytest
from src.book import Book
from src.member import Member, MemberCategory
from src.library import Library
from src.loan import LoanRecord, calculate_late_fee
from src.reservation import Reservation, ReservationManager


def test_member_category_non_string_invalid_type():
    with pytest.raises(ValueError, match="Invalid member category"):
        Member("M001", "Invalid Type", category=999)


def test_member_negative_fee_rate_raises():
    with pytest.raises(ValueError, match="Daily fee rate must be non-negative"):
        Member("M001", "Negative Rate", daily_fee_rate=-0.5)


def test_calculate_late_fee_with_custom_due_date():
    loan = LoanRecord(
        "L1",
        "M1",
        "1234567890",
        borrow_date=date(2026, 1, 1),
        due_date=date(2026, 1, 20),
    )
    assert loan.due_date == date(2026, 1, 20)
    loan.due_date = None
    assert calculate_late_fee(loan) == 0.0


def test_reservation_manager_branches():
    mgr = ReservationManager()
    # notify on empty queue
    assert mgr.notify_next("UNKNOWN_ISBN") is None
    # cancel on empty queue
    assert mgr.cancel_reservation("M001", "UNKNOWN_ISBN") is False

    # Queue with non-pending status ignored
    r = Reservation("R1", "M001", "1234567890", status="FULFILLED")
    mgr.add_reservation(r)
    assert mgr.get_queue("1234567890") == []
    assert mgr.cancel_reservation("M001", "1234567890") is False
    assert mgr.notify_next("1234567890") is None


def test_member_history_with_multiple_different_members():
    lib = Library()
    b = Book("1234567890", "Book", "Author")
    m1 = Member("M1", "Alice")
    m2 = Member("M2", "Bob")
    lib.add_book(b)
    lib.register_member(m1)
    lib.register_member(m2)

    lib.borrow_book("M1", "1234567890")
    # History for M2 is empty while M1 has 1 loan
    assert lib.get_member_history("M2") == []
    assert len(lib.get_member_history("M1")) == 1


def test_return_book_without_active_loan_record():
    lib = Library()
    b = Book("1234567890", "Book", "Author")
    m = Member("M1", "Alice")
    lib.add_book(b)
    lib.register_member(m)

    # Member manually has book in borrowed_books but no loan record in lib.loans
    m.borrowed_books.append("1234567890")
    b.available_copies -= 1
    assert lib.return_book("M1", "1234567890") is True


def test_return_book_matching_correct_loan_among_multiple():
    lib = Library()
    b1 = Book("1111111111", "Book 1", "Author", total_copies=2)
    b2 = Book("2222222222", "Book 2", "Author", total_copies=2)
    m = Member("M1", "Alice", max_borrow_limit=5)
    lib.add_book(b1)
    lib.add_book(b2)
    lib.register_member(m)

    # Alice borrows Book 1 then Book 2
    lib.borrow_book("M1", "1111111111", borrow_date=date(2026, 1, 1))
    lib.borrow_book("M1", "2222222222", borrow_date=date(2026, 1, 2))

    # Returning Book 1 exercises the branch where loan is Alice's but isbn != 1111111111
    assert lib.return_book("M1", "1111111111", return_date=date(2026, 1, 10)) is True
    assert "1111111111" not in m.borrowed_books
    assert "2222222222" in m.borrowed_books
