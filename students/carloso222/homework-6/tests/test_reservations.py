"""Advanced feature 2: reservation queue (FIFO) with notification on return."""

import pytest

from src.exceptions import ReservationError
from src.library import Library
from tests.conftest import CLEAN_CODE, REFACTORING


def test_member_can_reserve_an_unavailable_book(library):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    assert library.get_reservation_queue(REFACTORING) == ["S2"]


def test_reserve_book_returns_position_in_queue(library):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    assert library.reserve_book("F1", REFACTORING) == 2


def test_cannot_reserve_a_book_that_is_available(library):
    with pytest.raises(ReservationError, match="available"):
        library.reserve_book("S1", CLEAN_CODE)


def test_cannot_reserve_the_same_book_twice(library):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    with pytest.raises(ReservationError, match="already reserved"):
        library.reserve_book("S2", REFACTORING)


def test_cannot_reserve_a_book_you_already_hold(library):
    library.borrow_book("S1", REFACTORING)
    with pytest.raises(ReservationError, match="already has"):
        library.reserve_book("S1", REFACTORING)


def test_queue_is_empty_for_book_without_reservations(library):
    assert library.get_reservation_queue(CLEAN_CODE) == []


def test_first_member_in_queue_is_notified_when_book_returns(library, notifier):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    library.reserve_book("F1", REFACTORING)
    library.return_book("S1", REFACTORING)
    notifier.assert_called_once_with("S2", REFACTORING)


def test_no_notification_when_nobody_reserved(library, notifier):
    library.borrow_book("S1", REFACTORING)
    library.return_book("S1", REFACTORING)
    notifier.assert_not_called()


def test_returned_reserved_book_is_held_for_first_in_queue(library):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    library.return_book("S1", REFACTORING)
    with pytest.raises(ReservationError, match="held for member S2"):
        library.borrow_book("F1", REFACTORING)


def test_first_in_queue_can_borrow_and_leaves_the_queue(library):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    library.reserve_book("F1", REFACTORING)
    library.return_book("S1", REFACTORING)
    library.borrow_book("S2", REFACTORING)
    assert library.get_reservation_queue(REFACTORING) == ["F1"]


def test_queue_is_served_in_fifo_order(library, notifier):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    library.reserve_book("F1", REFACTORING)
    library.return_book("S1", REFACTORING)
    library.borrow_book("S2", REFACTORING)
    library.return_book("S2", REFACTORING)
    assert notifier.call_args_list[-1].args == ("F1", REFACTORING)


def test_library_without_notifier_still_handles_returns(library):
    quiet = Library()
    quiet.add_book(library.get_book(REFACTORING))
    quiet.register_member(library.get_member("S1"))
    quiet.register_member(library.get_member("S2"))
    quiet.borrow_book("S1", REFACTORING)
    quiet.reserve_book("S2", REFACTORING)
    quiet.return_book("S1", REFACTORING)
    assert quiet.get_book(REFACTORING).is_available() is True
