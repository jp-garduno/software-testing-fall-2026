import pytest
from src.book import Book
from src.member import Member
from src.library import Library


def test_reserve_available_book_raises_error():
    lib = Library()
    book = Book("1234567890", "Design Patterns", "GoF", total_copies=1)
    member = Member("M001", "Alice")
    lib.add_book(book)
    lib.register_member(member)

    with pytest.raises(ValueError, match="Cannot reserve a book with available copies"):
        lib.reserve_book("M001", "1234567890")


def test_reserve_book_success_when_unavailable():
    lib = Library()
    book = Book("1234567890", "Design Patterns", "GoF", total_copies=1)
    member1 = Member("M001", "Alice")
    member2 = Member("M002", "Bob")
    lib.add_book(book)
    lib.register_member(member1)
    lib.register_member(member2)

    lib.borrow_book("M001", "1234567890")
    res = lib.reserve_book("M002", "1234567890")
    assert res["status"] == "PENDING"
    assert res["member_id"] == "M002"
    assert res["isbn"] == "1234567890"
    assert lib.get_book_reservations("1234567890") == ["M002"]


def test_reserve_book_rejects_duplicate_or_current_borrower():
    lib = Library()
    book = Book("1234567890", "Design Patterns", "GoF", total_copies=1)
    member1 = Member("M001", "Alice")
    member2 = Member("M002", "Bob")
    lib.add_book(book)
    lib.register_member(member1)
    lib.register_member(member2)

    lib.borrow_book("M001", "1234567890")
    with pytest.raises(ValueError, match="Member currently holds a copy of this book"):
        lib.reserve_book("M001", "1234567890")

    lib.reserve_book("M002", "1234567890")
    with pytest.raises(ValueError, match="Book is already reserved by this member"):
        lib.reserve_book("M002", "1234567890")


def test_reserve_book_fifo_order_and_notification_on_return():
    lib = Library()
    book = Book("1234567890", "Design Patterns", "GoF", total_copies=1)
    m1 = Member("M001", "Alice")
    m2 = Member("M002", "Bob")
    m3 = Member("M003", "Charlie")
    lib.add_book(book)
    lib.register_member(m1)
    lib.register_member(m2)
    lib.register_member(m3)

    lib.borrow_book("M001", "1234567890")
    lib.reserve_book("M002", "1234567890")
    lib.reserve_book("M003", "1234567890")

    assert lib.get_book_reservations("1234567890") == ["M002", "M003"]

    # When Alice returns book, next person (Bob) is notified
    notified = lib.return_book("M001", "1234567890")
    assert lib.get_next_reservation_notification("1234567890") == "M002"
    assert lib.get_book_reservations("1234567890") == ["M003"]


def test_cancel_reservation_removes_from_queue():
    lib = Library()
    book = Book("1234567890", "Design Patterns", "GoF", total_copies=1)
    m1 = Member("M001", "Alice")
    m2 = Member("M002", "Bob")
    lib.add_book(book)
    lib.register_member(m1)
    lib.register_member(m2)

    lib.borrow_book("M001", "1234567890")
    lib.reserve_book("M002", "1234567890")
    assert lib.cancel_reservation("M002", "1234567890") is True
    assert lib.get_book_reservations("1234567890") == []
