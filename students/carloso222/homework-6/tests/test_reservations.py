"""Advanced feature 2: reservation queue (FIFO) with notification on return."""

import pytest

from src.exceptions import ReservationError
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
